from langchain.tools import tool

from app.services.mpg_prediction.mpg_prediction import predict_mileage
from app.utils.app_exception_handler import ApplicationException
from app.utils.applogger import logger


@tool(description="Predicts the miles per gallon (MPG) of a car based on its displacement, horsepower, and weight.")
def predict_mpg(displacement, horsepower, weight):
    """
    Predicts the miles per gallon (MPG) of a car based on its displacement, horsepower, and weight.

    :param displacement: The displacement of the car's engine in cubic inches.
    :param horsepower: The horsepower of the car's engine.
    :param weight: The weight of the car in pounds.
    :return: The predicted MPG of the car.
    """
    logger.info(f"user query displacement {displacement} horsepower {horsepower} weight {weight}")
    logger.info(f"calling from predict_mpg -> predict_mileage ")
    return predict_mileage(displacement, horsepower, weight)


def get_ml_tools():
    try:
        logger.info(f"calling get_ml_tools")
        return [predict_mpg]
    except Exception as e:
        logger.exception(f"error in get_ml_tools {e}")
        raise ApplicationException(status_code=500, detail="error in get_ml_tools")
