import pandas as pd
import os
import requests
import sys
from dateutil.parser import parse


if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    # write your code here
    def find_birth_country(row):
        country = row['place_of_birth']
        if country:
            if "," in country:
                country = country.split(',')
                country = [place.strip() for place in country]
                country = country.pop()
            else:
                country = None
        return country


    def fill_born_in(row):
        born_in = row['born_in']
        if not born_in or born_in.strip() == "":
            born_in = row['place_of_birth']
        return born_in


    def format_country_name(row):
        country = row['born_in']
        if country in ["US", "United States", "U.S."]:
            country = "USA"
        if country == "United Kingdom":
            country = "UK"
        return country

    def extract_birth_year(row):
        birth_date = row['date_of_birth']
        date = parse(birth_date)
        return date.year

    def calculate_winning_age(row):
        birth_year = row['year_born']
        winning_year = row['year']
        return winning_year - birth_year


    df = pd.read_json("../Data/Nobel_laureates.json")  # 1
    df.dropna(subset=['gender'], inplace=True)
    df['place_of_birth'] = df.apply(find_birth_country, axis=1)
    df['born_in'] = df.apply(fill_born_in, axis=1)
    df.dropna(subset=['born_in'], inplace=True)
    df['born_in'] = df.apply(format_country_name, axis=1)

    df['year_born'] = df.apply(extract_birth_year, axis=1)
    df['age_of_winning'] = df.apply(calculate_winning_age, axis=1)
    print(df['year_born'].tolist())
    print(df['age_of_winning'].tolist())

