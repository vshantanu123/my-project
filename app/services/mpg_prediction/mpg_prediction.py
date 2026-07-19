import json
from typing import Union

import joblib
import pandas as pd
from fastapi import HTTPException


def predict_mileage(displacement, horsepower, weight) -> Union[float | int | None]:
    """
    this tool will predict mpg of a vehicle
    provide the torque or displacement and horsepower and weight of the vehicle
    :param displacement: int
    :param horsepower: int
    :param weight: float
    :return: float
    """
    try:
        input_features = pd.DataFrame({
            "displacement": displacement,
            "horsepower": horsepower,
            "weight": weight
        }, index=[0])
        model = joblib.load("./app/services/mpg_prediction/mpg_predict_model.jlib")
        value = model.predict(input_features).item()
        _data = f"The mpg of the vehicle has displacement:{displacement}, horsepower:{horsepower} and weight:{weight} is {round(float(value), 2)}"
        return _data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error in predicting mpg {e}")
