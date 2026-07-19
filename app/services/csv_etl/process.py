import pandas as pd

file_path = "./app/datasets/csv/country_facts.csv"

cf_df = pd.read_csv(file_path, sep=",", encoding="utf-8")


def population_area_coastline_all_regions():
    """
        this function will return the sum of population, area and coastline of all regions
    """
    global cf_df
    region_df = cf_df.groupby("region")[['population', 'area', 'coastline']].sum().reset_index()
    _result = pd.DataFrame(region_df)
    _result = "".join(_result.to_string())
    return _result


def calculate_country_demographic(country_name: str):
    """
    calculate the agriculture, industry, service values of a country
    this function will return the demographic values of csv datasets of country facts
    """
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
    return _result


def countries_by_region_name(region_name: str):
    """
    this function will return the unique countries of a region
    """
    try:
        global cf_df
        new_df = cf_df.query(f"region.str.contains('{region_name.upper()}')")
        new_df = pd.DataFrame(new_df["country"].unique())
        _result = "".join(new_df.to_string())
        return _result
    except Exception as e:
        print(f"exception in getting countries by region {e}")


def countries_by_all_regions():
    """
    this function will return the unique countries of all regions
    """
    global cf_df
    _result = pd.DataFrame(cf_df.groupby("region")['country'].unique().reset_index())
    _result = "".join(_result.to_string())
    return _result
