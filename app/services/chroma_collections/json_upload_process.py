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
    return Chroma(
        collection_name="json_collection",
        persist_directory=get_value_from_key("CHROMA_DB_PATH")
        , embedding_function=embedding_model())


def save_json_document(filename):
    try:
        logger.info(f"loading json document {filename}")
        with open(f"./uploaded_documents/{filename}", "r+") as f:
            data = json.load(f)

        documents = []
        meta_datas = []
        _ids = []

        for idx, item in enumerate(data, start=1):
            documents.append(item["description"])
            documents.append(item["category"])
            _ids.append(str(idx))
            meta_datas.append({
                "name": item["name"],
                "price": item["price"],
                "category": item["category"],
            })
            # print(f"loaded {idx} json document description {item['description']}")

        chroma_client = chromadb.PersistentClient(path=get_value_from_key("CHROMA_DB_PATH"))
        embed_function = (embedding_functions
                          .SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2"))

        collection = chroma_client.get_or_create_collection(name="json_vector_db",
                                                            embedding_function=embed_function)
        collection.add(
            ids=_ids,
            documents=documents,
            metadatas=meta_datas
        )
        logger.info(f"done .... loading json document {filename}")
    except Exception as e:
        logger.exception(f"error in load json document {e}", )
        os.remove(f"./uploaded_documents/{filename}")
        raise HTTPException(status_code=500, detail="error in load json document ")


def search_chroma_for_json_content(query_str):
    try:
        chroma_client = chromadb.PersistentClient(path=get_value_from_key("CHROMA_DB_PATH"))
        collection = chroma_client.get_collection("json_vector_db")
        query_result = collection.query(query_texts=[query_str], n_results=10)
        logger.info(f"query result {query_result}")
        all_result_documents = query_result["documents"][0]
        str_all = "\n".join(all_result_documents)
        return str_all
    except Exception as e:
        logger.exception(f"error in search similarities in json schema {e}", )
        raise HTTPException(status_code=500, detail=f"error in search similarities json schema")
