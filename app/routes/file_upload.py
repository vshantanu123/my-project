import os

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.chroma_collections.json_upload_process import save_json_document
from app.services.chroma_collections.pdf_upload_process import save_embeddings_chromadb
from app.utils import get_message_from_key
from app.utils.applogger import logger

file_upload_router = APIRouter(prefix="/document", tags=["document"])


@file_upload_router.post("/Upload-document")
async def upload_document(file: UploadFile = File(...)):
    """
    upload a file to the server and cretate embeddings for the file (.pdf, .csv, .json)
    :param file: upload file
    :return: stream response
    """
    vector_store = None
    try:
        logger.info(f"Uploading and Processing File {file.filename}")
        upload_dir = "./uploaded_documents/"
        file_name = upload_dir + str(file.filename)

        upload_file_name = str(file.filename)
        ends_with = (".pdf", ".txt", ".csv", ".json")

        if not upload_file_name.endswith(ends_with):
            message = get_message_from_key("DOCUMENT_TYPE_NOT_SUPPORTED")
            logger.exception(f"exception -> {message} ")
            raise HTTPException(status_code=400, detail=f"{message}")
        elif os.path.isfile(file_name):
            message = get_message_from_key("DOCUMENT_EXISTS")
            logger.exception(f"exception -> {message}")
            raise HTTPException(status_code=400, detail=f"{message}")

        logger.info(f"writing file {file.filename} to uploaded_documents folder")

        with open(file_name, "wb") as buffer:
            buffer.write(file.file.read())

        logger.info(f"done uploading {file.filename} to folder")

        if file.content_type == "application/pdf":
            logger.info(f"creating vector for {file.filename} ")
            save_embeddings_chromadb(filename=upload_file_name)
        elif file.content_type == "application/json":
            logger.info(f"creating vector for {file.filename} ")
            save_json_document(filename=upload_file_name)

        return {"message": f"file {file.filename} of content type {file.content_type} uploaded successfully"}
    finally:
        logger.info(f"exiting from upload_document rest endpoint")
