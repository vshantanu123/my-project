import os

from fastapi import APIRouter, UploadFile, File
from fastapi.exceptions import HTTPException
from app.services.chroma_collections.json_upload_process import save_json_document
from app.services.chroma_collections.pdf_upload_process import save_embeddings_chromadb
from app.utils import get_message_from_key, get_value_from_key
from app.utils.applogger import logger

file_upload_router = APIRouter(prefix="/document", tags=["document"])


@file_upload_router.post("/Upload-document")
async def upload_document(file: UploadFile = File(...)):
    """
    upload a file to the server and create embeddings for the file (.pdf, .csv, .json)
    :param file: upload file
    :return: stream response
    """

    try:
        logger.info(f"Uploading and Processing File {file.filename}")
        upload_dir = get_value_from_key("UPLOADED_DOCS_PATH")
        file_name = f"{upload_dir}{file.filename}"
        upload_file_name = str(file.filename)
        ends_with = (".pdf", ".json")
        ### check if file is pdf or json
        if not upload_file_name.endswith(ends_with):
            message = get_message_from_key("DOCUMENT_TYPE_NOT_SUPPORTED")
            logger.exception(f"exception -> {message} ")
            raise HTTPException(status_code=500, detail=f"{message}")
        elif os.path.isfile(file_name):
            message = get_message_from_key("DOCUMENT_EXISTS")
            logger.exception(f"exception -> {message}")
            raise HTTPException(status_code=500, detail=f"{message}")

        logger.info(f"writing file {file.filename} to uploaded documents folder")

        ### write file to disk
        with open(file_name, "wb") as buffer:
            buffer.write(file.file.read())

        logger.info(f"done uploading {file.filename} to folder")

        ### create vector embeddings
        if file.content_type == "application/pdf":
            logger.info(f"creating vector for {file.filename} ")
            save_embeddings_chromadb(filename=upload_file_name)
        elif file.content_type == "application/json":
            logger.info(f"creating vector for {file.filename} ")
            save_json_document(filename=upload_file_name)

        return {"message": f"file {file.filename} of content type {file.content_type} uploaded successfully"}
    except Exception as e:
        logger.exception(f"error in upload_document rest endpoint {e}")
        return {f"message": f"{e}"}
    finally:
        logger.info(f"exiting from upload_document rest endpoint")
