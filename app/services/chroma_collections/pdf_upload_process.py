import os

from fastapi import HTTPException
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services import embedding_model
from app.utils import get_value_from_key
from app.utils.applogger import logger


def load_pdf_document(full_file_name):
    upload_dir = get_value_from_key("UPLOADED_DOCS_PATH")
    try:
        logger.info(f"loading pdf document {full_file_name}")
        pdf_loader = PyPDFLoader(f"{upload_dir}{full_file_name}")
        raw_docs = pdf_loader.load()
        logger.info(f"done .... loading pdf document {full_file_name}")
        return raw_docs
    except Exception as e:
        logger.exception(f"error in load_pdf_document {e}", )
        raise HTTPException(status_code=500, detail="error in load_pdf_document")


def create_embed_doc(raw_doc, chunk_size=1000, chunk_overlap=250):
    try:
        logger.info(f"creating embedd document")
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        documents = splitter.split_documents(raw_doc)
        logger.info(f"done .... creating embedd document")
        return documents
    except Exception as e:
        logger.exception(f"error in create embedd document {e}", )
        raise HTTPException(status_code=500, detail=f"error in create embedd document")


def save_embeddings_chromadb(filename):
    try:
        raw_doc = load_pdf_document(filename)
        documents = create_embed_doc(raw_doc)
        vector_store = Chroma.from_documents(
            collection_name="vector_db_collection",
            create_collection_if_not_exists=True,
            persist_directory=get_value_from_key("CHROMA_DB_PATH"),
            documents=documents,
            embedding=embedding_model())
    except Exception as e:
        logger.exception(f"error in save embeddings in chroma {e}", )
        os.remove(f"{upload_dir}{filename}")
        raise HTTPException(status_code=500, detail=f"error in save embedding in chroma")


def search_chroma_for_pdf_content(query_str):
    try:
        conn = Chroma(
            collection_name="vector_db_collection",
            persist_directory=get_value_from_key("CHROMA_DB_PATH"),
            embedding_function=embedding_model())
        matching_results = conn.similarity_search(query_str, k=1)
        for document in matching_results:
            return document.page_content
    except Exception as e:
        logger.exception(f"error in search similarities {e}", )
        raise HTTPException(status_code=500, detail=f"error in search similarities")
