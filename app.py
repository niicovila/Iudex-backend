import sys
import os
import json
import asyncio
from typing import List, Optional, Tuple, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from fastapi.responses import JSONResponse


# -------------------------------------------------------------------
# Initialize Services and Global Objects
# -------------------------------------------------------------------

app = FastAPI(docs_url=None, redoc_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/llm_output")
async def get_llm_output(file1: UploadFile = File(...), file2: UploadFile = File(...), file3: UploadFile = File(...)):
    # Process the files as needed
    # For example, read the contents
    contents1 = await file1.read()
    contents2 = await file2.read()
    contents3 = await file3.read()

    # Example response
    return {"response": [{'id': '*0*', 'value': '*0*', 'code': 12344}]}


# -------------------------------------------------------------------
# Main entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
