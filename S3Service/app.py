from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from S3Service import S3Service

app = FastAPI()
# Instantiate S3 Service
s3_service = S3Service()

# Request Models
class CreateFolderRequest(BaseModel):
    folder_name: str

class DeleteRequest(BaseModel):
    object_name: str

# FastAPI Endpoints

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), object_name: Optional[str] = Form(None)):
    """Upload a file to S3"""
    object_name = object_name or file.filename
    return s3_service.upload_file(file.file, object_name)

@app.post("/create-folder/")
async def create_folder(request: CreateFolderRequest):
    """Create a folder in S3"""
    return s3_service.create_folder(request.folder_name)

@app.delete("/delete-file/")
async def delete_file(request: DeleteRequest):
    """Delete a file from S3"""
    return s3_service.delete_file(request.object_name)

@app.delete("/delete-folder/")
async def delete_folder(request: DeleteRequest):
    """Delete a folder and its contents from S3"""
    return s3_service.delete_folder(request.object_name)