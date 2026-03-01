from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter()

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

@router.get("/images/{blob_name}")
async def get_image(blob_name: str):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        stream = blob_client.download_blob()

        def iterfile():
            for chunk in stream.chunks():
                yield chunk

        return StreamingResponse(iterfile(), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image not found")

@router.get("/images")
async def get_all_images():
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()
        images = []
        for blob in blob_list:
            images.append(blob.name)
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/images/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        new_container_name = "new-container-name"  # Replace with your new container name
        # Generate the new container name with the current date
        new_container_name = f"processed-img-{datetime.now().strftime('%m%d')}"
        new_blob_client = blob_service_client.get_blob_client(container=new_container_name, blob=file.filename)
        
        # Create the container if it doesn't exist
        container_client = blob_service_client.get_container_client(new_container_name)
        try:
            container_client.create_container()
        except Exception as e:
            pass  # Container already exists

        # Upload the file
        new_blob_client.upload_blob(file.file, overwrite=True)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))