# Import Libraries
import os
from dotenv import load_dotenv, dotenv_values
# import openai
# import re
from typing import List
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import math
# import requests

# Main function to ingest a document and store its embeddings
def ingest(UPLOAD_DIRECTORY: str, filename: str):
    dotenv_path = "D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/.env"
    OpenAI_TOKEN = load_env(dotenv_path)  # Load the OpenAI token
    
    file_path = f'{UPLOAD_DIRECTORY}/{filename}'  # Define the file path
    docs = read_document(file_path)  # Read the document
    
    splits = split_doc(docs, max_length=50)  # Split the document into chunks
    
    path = "D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/chroma"
    vectorstore_client = initialize_vector_store_client(path)  # Initialize the vector store client
    
    collection_name = f'{filename.rstrip(".txt").replace(" ","_")}_collection'
    model_name = "text-embedding-ada-002"
    
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OpenAI_TOKEN,
        model_name=model_name
    )  # Prepare the embedding function
    
    collection = prepare_collection(vectorstore_client, collection_name, openai_ef)  # Prepare the collection
    
    upsert_documents(collection, splits)  # Update/Insert the document splits
    
    return {
        "message": "New file ingested successfully",
        "collection_name": collection_name
    }

# Load environment variables from a .env file
def load_env(dotenv_path: str, override: bool = True) -> str:
    load_dotenv(dotenv_path=dotenv_path, override=override)
    return os.environ["OpenAI_TOKEN"]

# Read the content of a document from a given file path
def read_document(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as open_file:
        return open_file.read()

# Split the text into chunks of specified maximum length
def split_doc(docs: str, max_length: int = 50) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(max_length=max_length)
    return splitter.split_text(docs)

# Initialize the vector store client with a given path
def initialize_vector_store_client(path: str):
    return chromadb.PersistentClient(path=path)

# Prepare the collection and embedding function in the vector store
def prepare_collection(vectorstore_client, collection_name: str, openai_ef):
    return vectorstore_client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)

# Update/Insert document splits into the collection in batches with embeddings
def upsert_documents(collection, splits: List[str], batch_size: int = 2000):
    # Generate a list of unique IDs for each chunk
    ids = [str(id + 1) for id in range(len(splits))]
    loops = math.ceil(len(splits) / batch_size)  # Calculate the number of batches

    # Upsert each batch of document chunks
    for i in range(loops):
        collection.upsert(
            documents=splits[i * batch_size:(i + 1) * batch_size],
            ids=ids[i * batch_size:(i + 1) * batch_size]
        )

class RecursiveCharacterTextSplitter:
    def __init__(self, max_length: int, delimiters: List[str] = None):
        self.max_length = max_length
        self.delimiters = delimiters or ['\n\n', '\n', '.', '!', '?', ' ', '']

    def split_text(self, text: str) -> List[str]:
        return self._recursive_split(text, 0)

    def _recursive_split(self, text: str, delimiter_index: int) -> List[str]:
        if len(text) <= self.max_length:
            return [text]

        if delimiter_index >= len(self.delimiters):
            return [text[i:i+self.max_length] for i in range(0, len(text), self.max_length)]

        delimiter = self.delimiters[delimiter_index]
        if delimiter:
            parts = text.split(delimiter)
        else:
            parts = list(text)  # Split into individual characters if delimiter is empty

        splits = []
        current_split = ""

        for part in parts:
            if current_split and len(current_split) + len(part) + len(delimiter) > self.max_length:
                splits.append(current_split)
                current_split = part + delimiter
            else:
                current_split += part + delimiter

        if current_split:
            splits.append(current_split)

        # Further split splits that are too large
        final_splits = []
        for split in splits:
            if len(split) > self.max_length:
                final_splits.extend(self._recursive_split(split, delimiter_index + 1))
            else:
                final_splits.append(split)

        return final_splits


# def ingest(filename):
#     dotenv_path="D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/.env"
#     override=True
#     load_dotenv(dotenv_path=dotenv_path,override=override)
#     OpenAI_TOKEN = os.environ["OpenAI_TOKEN"]
#     url = f'uploaded_files/{filename}'
#     with open(url, 'r', encoding='utf-8') as open_file:
#         docs = open_file.read()
#     splitter = RecursiveCharacterTextSplitter(max_length=50)
#     splits = splitter.split_text(docs)
#     path="D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/chroma"
#     vectorstore_client = chromadb.PersistentClient(
#         path=path
#     )
#     # collection_name = f'{filename.rstrip(".txt")}_collection'
#     collection_name = 'story_collection'
#     model_name="text-embedding-ada-002"
#     openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key=OpenAI_TOKEN,
#                 model_name=model_name
#             )
#     collection = vectorstore_client.get_or_create_collection(
#         name=collection_name,
#         embedding_function=openai_ef
#     )
#     ids = []
#     len(ids)
#     id = 1
#     for i, split in enumerate(splits):
#             ids.append(str(id))
#             id+=1
#     batch_size = 2000
#     loops = math.ceil((len(splits))/batch_size)
#     loops
#     for i in range(0,loops):
#         collection.upsert(
#             documents = splits[(i*batch_size):(batch_size*(i+1))],
#             ids=ids[i*batch_size:batch_size*(i+1)]
#             # embedding = OpenAIEmbeddings(api_key=OpenAI_TOKEN)
#             # embeddings = openai.embeddings.create()
#         )
#     return {"message": "New file ingested successfully"}
