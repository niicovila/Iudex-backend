from fastapi import FastAPI, UploadFile, File
from DUADocument import DUADocumentService
import os
app = FastAPI()

# Replace with the actual S3 service endpoint
S3_SERVICE_URL = os.getenv("S3_SERVICE_URL", "http://s3-service:8000")


dua_document_service = DUADocumentService(S3_SERVICE_URL)


@app.post("/dua/upload/")
async def upload_dua_document(file: UploadFile = File(...)):
    """Upload a new DUA document via the S3 service."""
    return dua_document_service.save_document(file)


@app.put("/dua/update/")
async def update_dua_document(file: UploadFile = File(...), object_name: str = "DUA/document.pdf"):
    """Update an existing DUA document via the S3 service."""
    return dua_document_service.update_document(file, object_name)


@app.get("/dua/validate/")
async def validate_dua_document(object_name: str):
    """Check if a DUA document is valid via the S3 service."""
    is_valid = dua_document_service.is_valid_document(object_name)
    return {"object_name": object_name, "is_valid": is_valid}
