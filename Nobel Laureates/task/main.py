import pandas as pd
import os
import requests
import sys
import numpy as np
from dateutil.parser import parse
import matplotlib.pyplot as plt


def plot_pie_chart():
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 12)
    ax.pie(pie_chart_data['counter'].tolist(),
           labels=pie_chart_data['born_in'].tolist(),
           autopct=format_pct,
           explode=exploded,
           colors=['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple'])
    plt.show()


def set_data_pie_chart():
    global pie_chart_data, exploded, total
    pie_chart_data = df.groupby('born_in').agg(counter=('born_in', 'count'))
    pie_chart_data.reset_index(inplace=True)
    pie_chart_data['born_in'] = pie_chart_data.apply(aggregate_countries, axis=1)
    pie_chart_data = pie_chart_data.groupby('born_in').agg(counter=('counter', 'sum'))
    pie_chart_data.sort_values(by='counter', ascending=False, inplace=True)
    pie_chart_data.reset_index(inplace=True)
    exploded = [0, 0, 0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    total = pie_chart_data['counter'].sum()


def plot_bar_chart():
    bar_chart_dataframe = df[df.category != '']
    bar_chart_data = bar_chart_dataframe.groupby(['category', 'gender']).agg(counter=('gender', 'count')).reset_index()
    categories = bar_chart_data['category'].categories().tolist()
    male_winners = bar_chart_data[bar_chart_data.gender == 'male']['counter'].tolist()
    female_winners = bar_chart_data[bar_chart_data.gender == 'female']['counter'].tolist()
    plt.figure(figsize=(10, 10))
    x_axis = np.arange(len(categories))
    plt.bar(x_axis - 0.2, male_winners, width=0.4, label='Males', color='blue')
    plt.bar(x_axis + 0.2, female_winners, width=0.4, label='Females', color='crimson')
    plt.xticks(x_axis, categories)
    plt.xlabel('Category', fontsize=14)
    plt.ylabel('Nobel Laureates Count', fontsize=14)
    plt.title("The total count of male and female Nobel Prize winners by categories", fontsize=20)
    plt.legend(loc='upper right')
    plt.show()


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


    def aggregate_countries(row):
        counter = row['counter']
        if counter < 25:
            return 'Other Countries'
        else:
            return row['born_in']


    def format_pct(x):
        return '{:.2f}%\n({:.0f})'.format(x, total * x / 100)


    df = pd.read_json("../Data/Nobel_laureates.json")  # 1
    df.dropna(subset=['gender'], inplace=True)
    df['place_of_birth'] = df.apply(find_birth_country, axis=1)
    df['born_in'] = df.apply(fill_born_in, axis=1)
    df.dropna(subset=['born_in'], inplace=True)
    df['born_in'] = df.apply(format_country_name, axis=1)

    df['year_born'] = df.apply(extract_birth_year, axis=1)
    df['age_of_winning'] = df.apply(calculate_winning_age, axis=1)

    # set_data_pie_chart()
    # plot_pie_chart()

    # plot_bar_chart()

    plt.figure(figsize=(10, 10))
    boxplot_dataframe = df[df.category != '']
    boxplot_dataframe = boxplot_dataframe[['category', 'age_of_winning']]
    categories = boxplot_dataframe['category'].unique()
    categories.sort()
    data = [boxplot_dataframe[boxplot_dataframe.category == category]['age_of_winning'] for category in
            categories]
    all_categories = pd.concat(data)
    data.append(all_categories)
    categories = np.append(categories, "All categories")
    plt.boxplot(data, labels=categories, showmeans=True)
    plt.title('Distribution of Ages by Category')
    plt.ylabel('Age of Obtaining the Nobel Prize', fontsize=14)
    plt.xticks(fontsize=20)
    plt.show()
