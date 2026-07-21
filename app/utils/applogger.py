import datetime
import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Union

from fastapi import HTTPException
from pythonjsonlogger.json import JsonFormatter

from app.utils import Constants

logger: logging.Logger = logging.getLogger(__name__)
stream_handler: logging.StreamHandler = None
file_logger: RotatingFileHandler = None


async def create_log_file_name() -> Union[str, None]:
    """
        get the project name and date.
        create a log file name.
        :return: created log file name.
    """
    try:
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_name: str = f"{Constants.LOG_DIR}{Constants.APPLICATION_NAME}{today_date}.log"
        return log_file_name

    except Exception as e:
        print(" ********** error in getting log dir and create log file name  ******", e)
        raise e


async def get_formatter() -> JsonFormatter:
    """
    create a JSON log format.
    :return: created format.
    """
    log_dict = {
        "timestamp": "%(asctime)s",
        "filename": "%(filename)s",
        "function_name": "%(funcName)s",
        "message": "%(message)s"
    }
    return JsonFormatter(json.dumps(log_dict, indent=4))


async def application_logger(log_type="file", level=logging.DEBUG):
    """
    application level logger configuration.
    :param log_type:file/console(default= 'file')
    :param level: log level (default=DEBUG).
    :return: logger with configuration.
    """
    try:
        global logger
        global stream_handler, file_logger
        logger.setLevel(level)
        if log_type == 'file':
            log_file_name = await create_log_file_name()
            if log_file_name is not None:
                file_logger = RotatingFileHandler(log_file_name, mode="a", encoding="utf-8", maxBytes=4000000,
                                                  backupCount=3)
                file_logger.setFormatter(await get_formatter())
                logger.addHandler(file_logger)
        else:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(await get_formatter())
            logger.addHandler(stream_handler)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def applogger_graceful_shutdown():
    """
    this function is used to gracefully shut down the logger and remove the handler.
    :return:
    """
    global logger, stream_handler, file_logger

    try:
        if stream_handler:
            stream_handler.flush()
            logger.removeHandler(stream_handler)
            stream_handler.close()
        if file_logger:
            file_logger.flush()
            logger.removeHandler(file_logger)
            file_logger.close()
        if logger:
            logging.shutdown()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
