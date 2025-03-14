from fastapi import FastAPI, UploadFile, HTTPException
from typing import Optional
import httpx
import os

class DUADocumentService:
    """Service for handling DUA (Data Use Agreement) documents via the existing S3 service API."""

    def __init__(self, S3_SERVICE_URL: str):
        self.client = httpx.Client(base_url=S3_SERVICE_URL)

    def is_valid_document(self, object_name: str) -> bool:
        """Check if the document exists and follows business rules via the S3 service."""
        response = self.client.get(f"/file-exists/?object_name={object_name}")
        if response.status_code == 404:
            return False
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        # Business rule: Check if the document has a valid extension
        valid_extensions = {".pdf", ".docx", ".txt"}
        if not any(object_name.endswith(ext) for ext in valid_extensions):
            return False

        return True

    def save_document(self, file: UploadFile, object_name: Optional[str] = None):
        """Save a new DUA document via the S3 service."""
        object_name = object_name or f"DUA/{file.filename}"

        # Check if file already exists
        response = self.client.get(f"/file-exists/?object_name={object_name}")
        if response.status_code == 200:
            raise HTTPException(status_code=400, detail="Document already exists.")

        # Upload file
        files = {"file": (file.filename, file.file, file.content_type)}
        response = self.client.post("/upload/", files=files)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()

    def update_document(self, file: UploadFile, object_name: str):
        """Update an existing DUA document via the S3 service."""
        # Check if the document exists
        response = self.client.get(f"/file-exists/?object_name={object_name}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Document not found.")

        # Upload the updated file
        files = {"file": (file.filename, file.file, file.content_type)}
        response = self.client.put(f"/upload/?object_name={object_name}", files=files)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()


