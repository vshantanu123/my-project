import os

from langchain_openai import ChatOpenAI

from app.utils import get_value_from_key


def open_ai_llm():
    _llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0, streaming=True,
                      api_key=get_value_from_key("OPENAI_API_KEY"))
    return _llm
