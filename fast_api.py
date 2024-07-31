# Import Libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from ingest import ingest
from collection_names import collection_names
from delete_collection import delete_collection
from retrieve import retrieve

# Create an instance of FAST API, named as "app"
app = FastAPI()

# Directory to store uploaded files
UPLOAD_DIRECTORY = "uploaded_files"

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Function to update uploaded files list
def update_uploaded_files():
    uploaded_files = []
    for file_name in os.listdir(UPLOAD_DIRECTORY):
        if os.path.isfile(os.path.join(UPLOAD_DIRECTORY, file_name)):
            uploaded_files.append(file_name)
    return uploaded_files

# List to keep track of uploaded files
uploaded_files = update_uploaded_files()

@app.get('/')
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {
        'message': 'This is an FAST API trial',
        'data': 929
    }
   
# Upload and ingest a file
@app.post("/ingest/")
async def ingest_file(file: UploadFile = File(...)):
    """
    Endpoint to upload and ingest a file.
    """
    try:
        # Define the file location
        file_name_updated = file.filename.replace("_"," ")
        file_location = os.path.join(UPLOAD_DIRECTORY, file_name_updated)
        
        # Write the uploaded file to the specified location
        with open(file_location, "wb") as txt_file:
            txt_file.write(await file.read())

        # Call the ingest function to ingest the file
        ingest(UPLOAD_DIRECTORY, file_name_updated)
        
        # Add the filename to the list of uploaded_files
        uploaded_files.append(file.filename)
        
        return {
            "filename": file.filename,
            "message": "New file uploaded and ingested successfully"
        }
    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload and ingest the file: {str(e)}"
        )

#Get all uploaded file and ingested collection names
@app.get("/ingest/")
async def get_file_and_collection_names():
    """
    Endpoint to get all uploaded file names.
    """
    try:
        available_collections = []
        available_collections = collection_names(available_collections)
        uploaded_files = update_uploaded_files()
        return {
            "files": uploaded_files,
            "collections": available_collections
        }
    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve file names: {str(e)}"
        )


# Send the question and retrieve the answer
@app.post("/retrieve/")
async def retrieve_answer(question: str, collection_name: str):
    """
    Endpoint to send a question and retrieve the answer.
    """
    try:
        # Call the retrieve function to retrieve the answer
        answer = retrieve(question, collection_name)
        
        return {
            "question": question,
            "message": "Retrieved successfully",
            "answer": answer
        }
    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve the answer: {str(e)}"
        )

@app.post("/delete_collection/")
async def delete_collec(collection_name: str):
    """
    Endpoint to upload and ingest a file.
    """
    try:
        # Call the delete function to delete the collection
        response = delete_collection(collection_name)
        
        file_name=collection_name.replace("_collection",".txt").replace("_"," ")
        file_path = os.path.join(UPLOAD_DIRECTORY,file_name)

        # Check if the file exists before trying to delete it
        if os.path.exists(file_path):
            os.remove(file_path)
        return {
            response["message"]
        }
    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete the collection: {str(e)}"
        )

# Update a file
# @app.put("/upload/")
# async def update_file(file: UploadFile = File(...)):
#     file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
#     with open(file_location, "wb") as txt_file:
#         txt_file.write(await file.read())
#     return {
#         "filename": file.filename,
#         "message": "File updated successfully"
#     }
    

# files = []

# # Get all files
# @app.get("/ingestion")
# async def get_files():
#     return {"files": files}

# # Get single file
# @app.get("/ingestion/{file_id}")
# async def get_file(file_id: int):
#     for file in files:
#         if file.id == file_id:
#             return {"file": file}
#     return {"message": "No files found"}

# # Upload a file
# @app.post("/ingestion")
# async def upload_files(file: File):
#     files.append(file)
#     return {"message": "The file has been uploaded"}

# # Update a file
# @app.put("/ingestion/{file_id}")
# async def update_file(file_id: int, file_obj: File):
#     for file in files:
#         if file.id == file_id:
#             file.id = file_id
#             file.content = file_obj.content
#             return {"file": file}
#     return {"message": "No files found to update"}

# # Delete a file
# @app.delete("/ingestion/{file_id}")
# async def delete_file(file_id: int):
#     for file in files:
#         if file.id == file_id:
#             files.remove(file)
#             return {"message": "File has been DELETED!"}
#     return {"message": "No files found"}


    



