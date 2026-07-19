from langchain.tools import tool

from app.services.chroma_collections.json_upload_process import search_chroma_for_json_content
from app.services.chroma_collections.pdf_upload_process import search_chroma_for_pdf_content
from app.utils.applogger import logger


@tool
def search_uploaded_menu_for_answers(user_query: str):
    """
        user questions on menu items like
        1. give me all menu
        2. vegeterian food, noodles
        3. price range of food
        returns the results
    """
    logger.info(f"user query {user_query}")
    logger.info(f"calling menu json data")
    return search_chroma_for_json_content(user_query)


@tool(description="search uploaded pdfs for answers if available")
def search_uploaded_pdfs_for_answers(user_query: str):
    """
      this tool will search uploaded pdfs for answers if available.
    :param user_query:
    :return:
    """
    logger.info(f"user query {user_query}")
    logger.info(f"calling search chroma for pdf content  ")
    return search_chroma_for_pdf_content(user_query)


def get_db_tools():
    return [search_uploaded_menu_for_answers, search_uploaded_pdfs_for_answers]
