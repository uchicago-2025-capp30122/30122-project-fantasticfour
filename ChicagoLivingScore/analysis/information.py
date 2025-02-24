from pathlib import Path
import pandas as pd

datapath = Path(__file__).parent.parent/'data/cleaned_data'


def get_norm_housing_price(zip: int)->float:
    '''
    input: zip code
    output: the normative house price per sqft of this zipcode area
    '''
    housing_path = datapath/'Housing_Data_Final.csv'
    house_df = pd.read_csv(housing_path) 
    rv = house_df[house_df["zipcode"] == zip]["norm_avg_price_per_sqft"]

    return rv

def get_absolute_housing_price(zip: int)->float:
    '''
    input: zip code
    output: the absolute house price per sqft of this zipcode area
    '''
    housing_path = datapath/'Housing_Data_Final.csv'
    house_df = pd.read_csv(housing_path) 
    rv = house_df[house_df["zipcode"] == zip]["avg_price_per_sqft"]

    return rv

def get_trafic_convenience(zip: int)->float:
    '''
    input: zip code
    output: the average minutes to work
    The higher the number is,the less traffic convenience the area has
    '''
    
    econ_path = datapath/'Hamza_data_randomized.csv'
    econ_df = pd.read_csv(econ_path) 
    rv = econ_df[econ_df["Zipcode"] == zip]["Mean travel time to work (minutes)"]

    return rv


def get_umemployment(zip: int)->float:
    '''
    input: zip code
    output: the unemployment rate
    '''
    
    econ_path = datapath/'Hamza_data_randomized.csv'
    econ_df = pd.read_csv(econ_path) 
    rv = econ_df[econ_df["Zipcode"] == zip]["Unemployed"]

    return rv

