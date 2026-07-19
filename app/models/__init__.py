from typing import Annotated, TypedDict, Any, List

from langgraph.graph.message import add_messages
from pydantic import BaseModel


class InputModel(BaseModel):
    """
      pydantic model for input questions.
      user sends questions in this format
      list of questions
    """
    questions: list[str]


class AppState(TypedDict):
    """
    App state for langgraph
    """
    messages: Annotated[List[Any], add_messages]
    pass


class Constants:
    LOG_DIR = "./logs/"
    APPLICATION_NAME = "my-project-service"
    PROPERTIES_FILE_PATH = "./resources/application.properties"
    MESSAGE_FILE_PATH = "./resources/messages.properties"
