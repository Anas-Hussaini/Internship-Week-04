#### RETRIEVAL and GENERATION ####
import os
from dotenv import load_dotenv
import chromadb
# import openai
import chromadb.utils.embedding_functions as embedding_functions
from openai import OpenAI

# Main function to retrieve an answer for the question
def retrieve(question: str, collection_name: str) -> str:
    dotenv_path = "D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/.env"
    OpenAI_TOKEN = load_env(dotenv_path)  # Load the OpenAI token
    
    # collection_name = 'story_collection'
    model_name = "text-embedding-ada-002"
    
    openai_ef = initialize_openai_embedding_function(OpenAI_TOKEN, model_name)  # Initialize the embedding function
    
    vectorstore_client = initialize_vector_store_client()  # Initialize the vector store client
    
    collection = vectorstore_client.get_or_create_collection(
        name=collection_name,
        embedding_function=openai_ef
    )  # Prepare the collection
    
    retriever = retrieve_documents(collection, question)  # Retrieve documents
    
    context = format_docs(retriever)  # Format the retrieved documents
    
    prompt = create_prompt(question, context)  # Create the prompt
    
    answer = get_openai_answer(OpenAI_TOKEN, prompt)  # Get the answer from OpenAI
    
    return answer

# Load environment variables from a .env file
def load_env(dotenv_path: str, override: bool = True) -> str:
    load_dotenv(dotenv_path=dotenv_path, override=override)
    return os.environ["OpenAI_TOKEN"]

# Initialize the OpenAI embedding function
def initialize_openai_embedding_function(api_key: str, model_name: str):
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=model_name
    )

# Initialize the vector store client
def initialize_vector_store_client():
    return chromadb.PersistentClient()

# Retrieve documents from the collection based on the query
def retrieve_documents(collection, question: str, n_results: int = 5):
    return collection.query(query_texts=question, n_results=n_results)

# Format the retrieved documents into a single string
def format_docs(docs):
    return "\n\n".join(docs['documents'][0])

# Create a prompt for the OpenAI API based on the question and context
def create_prompt(question: str, context: str) -> str:
    # base_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    base_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Give detailed answers.

    Question: {} 

    Context: {} 

    Answer:
    """
    return base_prompt.format(question, context)

# Get an answer from OpenAI API based on the prompt
def get_openai_answer(api_key: str, prompt: str):
    openai_client = OpenAI(api_key=api_key)
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return openai_response.choices[0].message.content






# def retrieve(question):
#     dotenv_path="D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/.env"
#     override=True
#     load_dotenv(dotenv_path=dotenv_path,override=override)
#     OpenAI_TOKEN = os.environ["OpenAI_TOKEN"]
#     collection_name = 'story_collection'
#     model_name="text-embedding-ada-002"
#     openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key=OpenAI_TOKEN,
#                 model_name=model_name
#             )
#     vectorstore_client = chromadb.PersistentClient()
#     collection = vectorstore_client.get_or_create_collection(
#         name=collection_name,
#         embedding_function=openai_ef
#     )
#     retriever = collection.query(
#         query_texts=question,
#         n_results=3
#     )
#     def format_docs(docs):
#         return "\n\n".join(docs['documents'][0])
#     context = format_docs(retriever)
#     base_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

#     Question: {} 

#     Context: {} 

#     Answer:
#     """
#     prompt = f'{base_prompt.format(question, context)}'
#     openai_client = OpenAI(
#         api_key=OpenAI_TOKEN
#     )
    
#     openai_response = openai_client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[
#             {"role": "system", "content": prompt}
#         ]
#     )

#     answer = openai_response.choices[0].message.content
    
#     return answer
