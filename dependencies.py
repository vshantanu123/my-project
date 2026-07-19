from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.applogger import application_logger, applogger_graceful_shutdown

## cors origins
origins = ["*"]


## lifespan
@asynccontextmanager
async def life_span(app: FastAPI):
    """
        this is called when fastapi has been initialized at startup and shutdown event-yield the app.
        added @asynccontextmanager decorator so that : it will create a start event ... do stuff needed
        and return app and can do clean-up jobs later... if needed.
    :param app: FastAPI instance
    :return:app
    """
    print("starting my-project application")

    ## initialize application logger from util/applogger.py
    await application_logger()

    ## yield app
    yield
    ### shut down application logger
    applogger_graceful_shutdown()

    print("shutting down my-project application")
    pass


## cors middleware, allowing all origins
def initialize_middleware(app):
    """
        add cors middleware for connecting from react-application
        now it is open to call external sources/origins.
    :param app:
    :return:
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
