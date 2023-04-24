"""
- Automatically download datasets metadata from the ONS
- Get the titles of each dataset
- Find a description
- Get the column titles

Author: Rowan Trickett
Date: 13/04/2023
Last updated: 24/04/2023
"""

import requests
import pandas as pd
from io import StringIO
import json


"""
Starting with the ONS API

Notes:
- Column titles can't be easily obtained as it requires downloading the dataset -- will look into this further
"""

# Load ONS api and loops through all available datasets collecting their titles
def get_ONS_datasets_titles_descriptions():
    api_url = "https://api.beta.ons.gov.uk/v1/datasets"
    offset = 0
    max = 500
    titles = []
    descriptions = []

    if requests.get(api_url).status_code == 200:
        while len(titles) < max:
            response = requests.get(api_url, params={"offset": offset})
            #print(response.status_code)

            result = response.json()  # load json file
            r = result['items']
            for data in r:
                titles.append(data['title'])  # add dataset titles to a list
                descriptions.append(data['description']) # add dataset descriptions to a list

            offset += result['count']  # offset to avoid datasets already seen

            if result['count'] == 0:
                break

    else:
        titles = "Error: " + str(requests.get(api_url).status_code)
    
    return titles, descriptions


"""
Loads ONS api and loops through collecting their urls (that can be used to download a csv file of each one)

As an example, the first url refers to the file that can be found online here:
https://www.ons.gov.uk/datasets/wellbeing-quarterly/editions/time-series/versions/6
"""
def get_ONS_datasets_urls():
    api_url = "https://api.beta.ons.gov.uk/v1/datasets"
    offset = 0
    max = 500
    datasets_urls = []

    while len(datasets_urls) < max:
        response = requests.get(api_url, params={"offset": offset})
        result = response.json()

        r = result['items']
        for row in r:
            edition = row.get("links").get("latest_version").get("href")
            datasets_urls.append(edition)

        offset += result['count']  # offset to avoid datasets already seen

        if result['count'] == 0:
            break

    return datasets_urls


def find_ONS_cols(url):
    # Finding the csv download link for a specific dataset
    test = requests.get(url).json()

    if test.get('downloads'):
        temp_url = test.get("downloads").get("csv").get("href")

        # Has to be done like this to avoid HTTP 403 Error
        # Solution found at: https://datascience.stackexchange.com/questions/49751/read-csv-file-directly-from-url-how-to-fix-a-403-forbidden-error
        csv_url = requests.get(temp_url).text
        temp_df = pd.read_csv(StringIO(csv_url), dtype='string')
        col_headings = temp_df.columns
        col_headings = col_headings.to_list()
    else:
        col_headings = float('nan')  # This means the link did not have a csv file href

    return col_headings


"""
Nomis API

Function to get the names of all the datasets available via 
Nomis api.

Note:
Unfortunately the Nomis api requires we specify the parameters (such as 
geography, age, sex, etc) in order to form a uri and download a dataset.
These parameters change depending on the data we are dealing with making
automation very difficult.
"""
def get_nomis_datasets_titles_descriptions():
    url = "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json"
    response = requests.get(url)
    data = response.json()
    temp = data['structure']['keyfamilies']['keyfamily']
    nomis_datasets_names = []
    nomis_datasets_descriptions = []
    for dataset in temp:
        nomis_datasets_names.append(dataset['name']['value'])

        if 'description' in dataset:
            nomis_datasets_descriptions.append(dataset['description']['value'])
        else:
            nomis_datasets_descriptions.append(float('nan'))

    return nomis_datasets_names, nomis_datasets_descriptions


