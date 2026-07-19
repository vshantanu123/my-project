import json

import pandas as pd

file_path = "./app/datasets/json/college_admissions.json"
# file_path = "../../datasets/json/college_admissions.json"

college_admission_df = pd.read_json(file_path, encoding='utf-8')


def get_university_names():
    try:
        global college_admission_df
        _result = college_admission_df['university_name'].unique()
        all_str = "\n".join(_result.tolist())
        return all_str
    except Exception as e:
        print(e)


def get_universities_fees_less_than(total_amount: int):
    global college_admission_df
    _result = college_admission_df[
        (college_admission_df['total_instate_fee'] < total_amount) | (
                college_admission_df['total_outstate_fee'] < total_amount)][[
        "university_name", "total_instate_fee", "total_outstate_fee"]]
    _result = "".join(_result.to_string())
    return _result
