from fastapi import FastAPI

from app.routes.ai import ai_router
from app.routes.file_upload import file_upload_router
from dependencies import life_span, initialize_middleware
from app.utils.applogger import logger

# start the application by instantiating the FastAPI class, this calls the life_span function
# from dependencies.py
app = FastAPI(lifespan=life_span)

## add middleware for handling cors requests and loading all properties
initialize_middleware(app)

# add the routers
app.include_router(ai_router)

app.include_router(file_upload_router)


@app.get("/")
@app.get("/Health-Check", status_code=200)
async def home_main():
    """
    :return:
    """
    logger.info("starting main")
    return {"message": " My Project Submission Application Is Up And Running !!! "}
