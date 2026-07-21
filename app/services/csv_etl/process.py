import pandas as pd

from app.utils.app_exception_handler import ApplicationException
from app.utils.applogger import logger

file_path = "./app/datasets/csv/country_facts.csv"

cf_df = pd.read_csv(file_path, sep=",", encoding="utf-8")


def population_area_coastline_all_regions():
    """
        this function will return the sum of population, area and coastline of all regions
    """
    try:
        logger.info(f"calling population_area_coastline_all_regions")
        global cf_df
        region_df = cf_df.groupby("region")[['population', 'area', 'coastline']].sum().reset_index()
        _result = pd.DataFrame(region_df)
        _result = "".join(_result.to_string())
        logger.info(f"exiting population_area_coastline_all_regions")
        return _result
    except Exception as e:
        logger.exception(f"error in population_area_coastline_all_regions {e}")
        raise ApplicationException(status_code=500, detail="Error In Population area coastline all regions")


def calculate_country_demographic(country_name: str):
    """
    calculate the agriculture, industry, service values of a country
    this function will return the demographic values of csv datasets of country facts
    """
    try:
        logger.info(f"calling calculate_country_demographic for country {country_name}")
        global cf_df
        country_df = cf_df[cf_df['country'] == country_name]
        country_df = country_df[['population', 'agriculture', 'industry', 'service']]
        population = country_df['population']
        country_df['agri_val'] = population * country_df['agriculture'] / 100
        country_df['ind_val'] = population * country_df['industry'] / 100
        country_df['ser_val'] = population * country_df['service'] / 100
        country_df = country_df[['country', 'population', 'agri_val', 'ind_val', 'ser_val']]
        _result = pd.DataFrame(country_df)
        _result = "".join(_result.to_string())
        logger.info(f"exiting  calculate_country_demographic for country")
        return _result
    except Exception as e:
        logger.exception(f"error in calculate_country_demographic {e}")
        raise ApplicationException(status_code=500, detail="error in calculating country demographic")


def countries_by_region_name(region_name: str):
    """
    this function will return the unique countries of a region
    """
    try:
        logger.info(f"calling countries_by_region_name for region {region_name}")
        global cf_df
        new_df = cf_df.query(f"region.str.contains('{region_name.upper()}')")
        new_df = pd.DataFrame(new_df["country"].unique())
        _result = "".join(new_df.to_string())
        logger.info(f"exiting countries_by_region_name for region")
        return _result
    except Exception as e:
        logger.exception(f"error in countries_by_region_name {e}")
        raise ApplicationException(status_code=500, detail="error in error in countries_by_region_name")


def countries_by_all_regions():
    """
    this function will return the unique countries of all regions
    """
    try:
        logger.info(f"calling countries_by_all_regions")
        global cf_df
        _result = pd.DataFrame(cf_df.groupby("region")['country'].unique().reset_index())
        _result = "".join(_result.to_string())
        logger.info(f"exiting countries_by_all_regions")
        return _result
    except Exception as e:
        logger.exception(f"error in countries_by_all_regions {e}")
        raise ApplicationException(status_code=500, detail="error in countries_by_all_regions")
