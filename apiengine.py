import requests
import pandas as pd

class WorldBankData:
    def __init__(self):
        self.base_url = "http://api.worldbank.org/v2/country/{}/indicator/{}?date=1950:2020&format=json"
        self.countries = {'China': 'CHN', 'USA': 'USA', 'India': 'IND'}
        self.indicators = {'GDP': 'NY.GDP.MKTP.CD', 'Unemployment': 'SL.UEM.TOTL.ZS'}

    def fetch_data(self, country_code, indicator_code):
        url = self.base_url.format(country_code, indicator_code)
        response = requests.get(url)
        data = response.json()
        if len(data) == 2 and 'page' in data[0]:
            df = pd.DataFrame(data[1])
            df = df[['date', 'value']]
            df.columns = ['Year', indicator_code]
            return df
        else:
            return pd.DataFrame()

    def get_gdp_data(self):
        return {country: self.fetch_data(code, self.indicators['GDP']) for country, code in self.countries.items()}

    def get_unemployment_data(self):
        return {country: self.fetch_data(code, self.indicators['Unemployment']) for country, code in self.countries.items()}

    def create_datasets(self):
        gdp_data = self.get_gdp_data()
        unemployment_data = self.get_unemployment_data()

        gdp_dataset = pd.concat(gdp_data).reset_index().drop('level_1', axis=1)
        gdp_dataset.columns = ['Country', 'Year', 'GDP']

        unemployment_dataset = pd.concat(unemployment_data).reset_index().drop('level_1', axis=1)
        unemployment_dataset.columns = ['Country', 'Year', 'Unemployment']

        combined_dataset = pd.merge(gdp_dataset, unemployment_dataset, on=['Country', 'Year'])
        return gdp_dataset, unemployment_dataset, combined_dataset

