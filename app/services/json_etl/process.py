import pandas as pd

from app.utils.app_exception_handler import ApplicationException
from app.utils.applogger import logger

file_path = "./app/datasets/json/college_admissions.json"
# file_path = "../../datasets/json/college_admissions.json"

college_admission_df = pd.read_json(file_path, encoding='utf-8')


def get_university_names():
    """
    Returns a list of unique university names from the college admission dataset.
    """
    try:
        logger.info(f"calling get_university_names")
        global college_admission_df
        _result = college_admission_df['university_name'].unique()
        all_str = "\n".join(_result.tolist())
        logger.info(f"exiting get_university_names")
        return all_str
    except ApplicationException as e:
        logger.exception(f"error in get_university_names {e}")
        raise ApplicationException(status_code=500, detail="error in get_university_names")


def get_universities_fees_less_than(total_amount: int):
    """
    Returns a string representation of universities with fees less than the specified amount.
    """
    try:
        logger.info(f"calling get_universities_fees_less_than")
        global college_admission_df
        _result = college_admission_df[
            (college_admission_df['total_instate_fee'] < total_amount) | (
                    college_admission_df['total_outstate_fee'] < total_amount)][[
            "university_name", "total_instate_fee", "total_outstate_fee"]]
        _result = "".join(_result.to_string())
        logger.info(f"exiting get_universities_fees_less_than")
        return _result
    except ApplicationException as e:
        logger.exception(f"error in get_universities_fees_less_than {e}")
        raise ApplicationException(status_code=500, detail="error in get_universities_fees_less_than")
