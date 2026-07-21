import os

from langchain_openai import ChatOpenAI

from app.utils.app_exception_handler import ApplicationException


def open_ai_llm():
    try:
        os.environ["OPENAI_API_KEY"] = str(os.getenv("OPENAI_API_KEY"))
        _llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0, streaming=True)
        return _llm
    except Exception as e:
        raise ApplicationException(status_code=500, detail=f"{e}")