import chromadb
import os
import shutil

def delete_collection(collection_name: str):
    # Initialize the ChromaDB vectorstore_client
    path = "D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/chroma"
    vectorstore_client = chromadb.PersistentClient(path=path)
    vectorstore_client.delete_collection(name=collection_name)
    
    # collection_folder = os.path.join("chroma", collection_name)
    # if os.path.exists(collection_folder):
    #     shutil.rmtree(collection_folder)
    return{
        "message": f"{collection_name} has been deleted!"
    }



# collection = vectorstore_client.get_or_create_collection(name="Harry_Potter_and_The_Half_Blood_Prince_collection")
#     ids = collection.get()["ids"]
#     batch_size = 5461
#     loops = math.ceil(len(ids) / batch_size)
#     for i in range(loops):
#         collection.delete(
#             ids=ids[i * batch_size:(i + 1) * batch_size]
#         )