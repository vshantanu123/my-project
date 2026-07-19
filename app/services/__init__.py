import os

from langchain_openai import OpenAIEmbeddings

from app.utils import get_value_from_key
from app.utils.applogger import logger


def embedding_model():
    logger.info("getting embedding model")
    os.environ["OPENAI_API_KEY"] = get_value_from_key("OPENAI_API_KEY")
    embedder = OpenAIEmbeddings(model=get_value_from_key("EMBEDDING_MODEL"))
    logger.info("done ... getting embedding model")
    return embedder
