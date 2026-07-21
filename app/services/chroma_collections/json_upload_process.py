import json
import os

import chromadb
from chromadb.utils import embedding_functions
from fastapi import HTTPException
from langchain_chroma import Chroma

from app.services import embedding_model
from app.utils import get_value_from_key
from app.utils.applogger import logger


def get_vector_store():
    """
    Retrieves the Chroma vector store.

    Returns:
        Chroma: The Chroma vector store.
    """
    return Chroma(
        collection_name="json_collection",
        persist_directory=get_value_from_key("CHROMA_DB_PATH")
        , embedding_function=embedding_model())


def save_json_document(filename):
    """
    Saves a JSON document to the Chroma vector store.

    Args:
        filename (str): The name of the JSON file to be saved.

    Raises:
        HTTPException: If there is an error-loading the JSON document.
    """
    upload_dir = get_value_from_key("UPLOADED_DOCS_PATH")
    try:
        logger.info(f"loading json document {filename}")
        with open(f"{upload_dir}{filename}", "r+") as f:
            data = json.load(f)

        descriptions = []
        meta_datas = []
        _ids = []

        for _idx, item in enumerate(data, start=1):
            _ids.append(str(_idx))
            combined = f"description: {item["description"]} name: {item["name"]} price:{item["price"]} category:{item["category"]}"
            descriptions.append(combined.strip())
            meta_datas.append({
                "name": item["name"],
                "price": item["price"],
                "category": item["category"],
            })
            # print(f"loaded {idx} json document description {item['description']}")

        chroma_client = chromadb.PersistentClient(path=get_value_from_key("CHROMA_DB_PATH"))
        embed_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        collection = chroma_client.get_or_create_collection(name="json_vector_db", embedding_function=embed_function)

        # print(f"length of all docs {len(documents)}-> meta_datas {len(meta_datas)}-> ids {len(_ids)}")
        collection.add(documents=descriptions, metadatas=meta_datas, ids=_ids)

        logger.info(f"done .... loading json document {filename}")
    except Exception as e:
        logger.exception(f"error in load json document {e}")
        os.remove(f"{upload_dir}{filename}")
        raise HTTPException(status_code=500, detail="Error Loading Json Document ")


def search_chroma_for_json_content(query_str):
    """
    Searches the Chroma vector store for JSON content based on a query string.

    Args:
        query_str (str): The query string to search for.

    Returns:
        str: The retrieved JSON content.

    Raises:
        HTTPException: If there is an error in searching for similarities in the JSON schema.
    """
    try:
        chroma_client = chromadb.PersistentClient(path=get_value_from_key("CHROMA_DB_PATH"))
        collection = chroma_client.get_collection("json_vector_db")
        query_result = collection.query(query_texts=[query_str], n_results=10)
        logger.info(f"query result {query_result}")
        all_result_documents = query_result["documents"][0]
        str_all = "\n".join(all_result_documents)
        return str_all
    except Exception as e:
        logger.exception(f"error in search similarities in json schema {e}")
        raise HTTPException(status_code=500, detail=f"error in search similarities json schema")
