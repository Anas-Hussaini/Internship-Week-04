import chromadb
# import math

def collection_names(available_collections: list):
    # Initialize the ChromaDB vectorstore_client
    path = "D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/chroma"
    vectorstore_client = chromadb.PersistentClient(path=path)
    collections = vectorstore_client.list_collections()
    # vectorstore_client.reset()
    for collection in collections:
        # print(f"Name: {collection.name}")
        available_collections.append(collection.name)
    return available_collections

# # Initialize the ChromaDB vectorstore_client
# vectorstore_client = chromadb.PersistentClient(path = "D:/Data Science Projects/Scalence Internship ML/Bukhari-Muslim-RAG/chroma")

# # Create two collections
# collection1 = vectorstore_client.get_or_create_collection(name='StoryCollection1')
# collection2 = vectorstore_client.get_or_create_collection(name='StoryCollection2')

# # Dummy data: story embeddings (for example purposes, let's use random embeddings)
# # story_embeddings1 = [
# #     {'id': 'story1', 'embedding': [0.1, 0.2, 0.3], 'metadata': {'title': 'Story 1'}},
# #     {'id': 'story2', 'embedding': [0.4, 0.5, 0.6], 'metadata': {'title': 'Story 2'}}
# # ]

# # story_embeddings2 = [
# #     {'id': 'story3', 'embedding': [0.7, 0.8, 0.9], 'metadata': {'title': 'Story 3'}},
# #     {'id': 'story4', 'embedding': [0.1, 0.4, 0.7], 'metadata': {'title': 'Story 4'}}
# # ]

# # Add embeddings to the collections
# # collection1.add(story_embeddings1)
# collection1.add(
#     ids=["1","2","3","4","5"],
#     embeddings=[
#         [0.3,0.322,0.233,0.68233,0.212,0.68122],
#         [0.3,0.32862,0.4343,0.233,0.212,0.16822],
#         [0.3,0.3822,0.268833,0.2243387,0.212,0.122],
#         [0.3,0.34422,0.233,0.233,0.212,0.122],
#         [0.3,0.3262,0.3287233,0.233,0.234412,0.122]
#     ]
# )
# collection2.add(
#     ids=["1","2","3","4","5"],
#     embeddings=[
#         [0.3,0.562,0.233,0.68233,0.212,0.68122],
#         [0.3,0.32862,0.76343,0.233,0.212,0.022],
#         [0.3,0.3822,0.9833,0.07,0.212,0.122],
#         [0.3,0.34422,0.933,0.233,0.212,0.122],
#         [0.3,0.062,0.83,0.233,0.8412,0.02]
#     ]
# )


# # Retrieve and display the names of the collections created
# collections = vectorstore_client.list_collections()
# print("Collections created:")
# for collection in collections:
#     print(f"Name: {collection.name}")