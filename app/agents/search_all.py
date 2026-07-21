from fastapi.exceptions import HTTPException

from app.agents import open_ai_llm
from app.models import AppState
from app.tools.db_tools import get_db_tools
from app.tools.etl_tools import get_etl_tools
from app.tools.ml_tools import get_ml_tools
from app.utils.applogger import logger


def get_all_tools():
    """
        get all tools from all tools modules
    """
    try:
        etl_tools = get_etl_tools()
        db_tools = get_db_tools()
        ml_tools = get_ml_tools()
        merged_tools = [etl_tools, db_tools, ml_tools]
        return [tools for sublist in merged_tools for tools in sublist]
    except Exception as e:
        logger.exception(f"error in get_all_tools {e}")
        raise HTTPException(status_code=500, detail=str(e))


def search_for_all_queries(state: AppState):
    """
        search for all queries using all tools
    """
    try:
        logger.info(f"searching for all queries")
        _llm = open_ai_llm()
        llm_with_tools = _llm.bind_tools(get_all_tools())
        response = llm_with_tools.invoke(state["messages"])
        return {
            "messages": [response]
        }
    except Exception as e:
        logger.exception(f"error in search_for_all_queries {e}", )
        raise HTTPException(status_code=500, detail=str(e))
