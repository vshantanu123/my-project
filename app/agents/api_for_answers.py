from fastapi.exceptions import HTTPException
from langchain_core.messages import HumanMessage

from app.agents.graph_flow import graph_flow
from app.utils.applogger import logger


def call_this_api_for_all_your_answers(questions: list):
    """
        call this api for all your questions and get answers from the graph.
    :param questions: can be list of questions
    :return: the stream, in messages format
    """
    logger.info(f"got the questions {questions}")
    # get compiled graph app flow
    app_work_flow = graph_flow()

    try:
        input_messages = {"messages": [HumanMessage(content=message) for message in questions]}
        logger.info(f"invoking the graph with the questions {input_messages}")
        for mode, chunk in app_work_flow.stream(input=input_messages, stream_mode=["messages"]):
            if mode == "messages":
                token, meta_data = chunk
                if token.content and len(token.content) > 0:
                    yield from token.content
        yield "\n\n Done \n\n"

    except Exception as e:
        logger.exception(f"**** error in : call_this_api_for_all_your_answers ***{e}", )
        raise HTTPException(status_code=500, detail=f"error in fetching answers")
