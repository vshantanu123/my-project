from typing import Iterable, Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.agents.api_for_answers import call_this_api_for_all_your_answers
from app.models import InputModel
from app.utils.applogger import logger

ai_router = APIRouter(prefix="/ai", tags=["ai"])


@ai_router.post("/Ask-Questions", response_class=StreamingResponse)
def ask(inputs: InputModel) -> Iterable[Any]:
    logger.info(f"user has these questions {inputs.questions}")
    logger.info(f"calling api for answers")
    try:
        logger.info(f"question {inputs.questions}")
        return call_this_api_for_all_your_answers(inputs.questions)
        # return StreamingResponse(chunks, media_type="application/event-stream",
        #                          headers={"X-Accel-Buffering": "no"})
    except Exception as e:
        logger.exception(f"error in fetching answers {e}")
        raise HTTPException(status_code=500, detail=f"no answers found")
