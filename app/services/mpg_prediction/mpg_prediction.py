import joblib
import pandas as pd
from fastapi import HTTPException

from app.utils.app_exception_handler import ApplicationException
from app.utils.applogger import logger


def predict_mileage(displacement, horsepower, weight) -> str:
    """
    this tool will predict mpg of vehicle
    provide the torque or displacement and horsepower and weight of the vehicle
    :param displacement: int
    :param horsepower: int
    :param weight: float
    :return: float
    """
    try:
        logger.info(f"calling predict_mileage")
        input_features = pd.DataFrame({
            "displacement": displacement,
            "horsepower": horsepower,
            "weight": weight
        }, index=[0])
        model = joblib.load("./app/services/mpg_prediction/mpg_predict_model.jlib")
        value = model.predict(input_features).item()
        _data = f"The mpg of the vehicle has displacement:{displacement}, horsepower:{horsepower} and weight:{weight} is {round(float(value), 2)}"
        logger.info(f"mpg prediction {value}")
        return _data
    except Exception as e:
        logger.exception(f"error in predicting mpg {e}")
        raise ApplicationException(status_code=500, detail="error in predicting mpg")
