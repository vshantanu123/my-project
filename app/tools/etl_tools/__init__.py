####

###########
from langchain.tools import tool

from app.services.csv_etl.process import (countries_by_all_regions,
                                          countries_by_region_name, \
                                          population_area_coastline_all_regions,
                                          calculate_country_demographic)
from app.services.json_etl.process import get_university_names, get_universities_fees_less_than
from app.utils.applogger import logger


########## country specific
@tool(description="get all countries")
def get_all_countries():
    """
    get all countries
    :return:
    """
    logger.info(f"calling from get_all_countries -> countries_by_all_regions")
    _result = countries_by_all_regions()
    # print(f"All Country names -> {_result}")
    return _result


@tool(description="countries in region e.g. america, Asia")
def fetch_countries_region(region: str):
    """
        get all countries by region name
        example:
            list all countries in america
            countries in Asia
    """
    logger.info(f"user query  region name {region}")
    logger.info(f"calling from get_countries_by_region -> countries_by_region_name")
    _result = countries_by_region_name(region_name=region.upper())
    # print(f"countries by region names -> {_result}")
    return _result


@tool(description="get the population and coastline data for all regions")
def get_population_coastlines_by_region():
    """
    this function will return the population and coastline data for all regions.
    :return:
    """
    logger.info(f"calling from get_population_coastlines_by_region -> population_area_coastline_all_regions")
    _result = population_area_coastline_all_regions()
    # print(f"get population and coastline by region  -> {_result}")
    return _result


@tool(description="get the country demographic based on country name")
def calculate_demographic(country_name: str):
    """
       calculate the agriculture, industry, service values of a country
       example:
           calculate demographic data of India
           calculate demographic data of USA
           calculate the agriculture, industry, service values of a country
           calculate the agriculture, industry, service values of a country
    """
    logger.info(f"user query  country name {country_name}")
    logger.info(f"calling from calculate_demographic -> calculate_country_demographic")
    _result = calculate_country_demographic(country_name=country_name.lower().title())
    # print(f"calculated country demographic data is -> {_result}")
    return _result


###############
@tool(description="get all universities.")
def get_universities():
    """
     get all university names private and public.
    """
    logger.info(f"user query  university names")
    _result = get_university_names()
    # print(f"All university names {_result}")
    return _result


@tool(description="get the universities and their fees less than the price given.")
def get_university_fess_less_than_price_given(fees_price):
    """
    this tool will return the university names and their respective fees-price
    less than the price given.
    """
    logger.info(f"user query  fees {fees_price}")
    logger.info(f"get_university_fess_less_than_price_given")
    _result = get_universities_fees_less_than(fees_price)
    # print(f"University fees less than {fees_price} is -> {_result}")
    return _result


def get_etl_tools():
    return [get_universities, get_university_fess_less_than_price_given,
            get_all_countries, fetch_countries_region,
            get_population_coastlines_by_region, calculate_demographic]
