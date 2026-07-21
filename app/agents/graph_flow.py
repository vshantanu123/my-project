from fastapi import HTTPException
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agents.search_all import search_for_all_queries, get_all_tools
from app.models import AppState
from app.utils.applogger import logger


def graph_flow() -> CompiledStateGraph:
    try:
        logger.info(f"starting graph flow")
        tools = get_all_tools()
        logger.info(f"got all tools {tools}")

        tool_workflow = StateGraph(AppState)

        tool_workflow.add_node("search_for_answers", search_for_all_queries)
        tool_workflow.add_node("tools", ToolNode(tools))
        tool_workflow.add_edge(START, "search_for_answers")
        tool_workflow.add_conditional_edges("search_for_answers", tools_condition)
        tool_workflow.add_edge("tools", END)

        logger.info(f"added all the nodes and edges")
        logger.info(f"compiled the graph ----  return app")
        work_flow_app = tool_workflow.compile()
        return work_flow_app

    except Exception as e:
        logger.exception(f"error in graph_flow {e}")
        raise HTTPException(status_code=500, detail=str(e))
