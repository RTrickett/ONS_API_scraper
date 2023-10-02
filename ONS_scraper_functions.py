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
from bs4 import BeautifulSoup
import re


"""
Starting with the ONS API

Notes:
- Column titles can't be easily obtained as it requires downloading the dataset -- will look into this further
"""

# Load ONS api and loops through all available datasets collecting their titles
def get_ONS_datasets_titles_descriptions():
    """Load ONS api and loop through all available datasets 
    collecting their titles and a short description."""
    api_url = "https://api.beta.ons.gov.uk/v1/datasets"
    offset = 0
    max = 500
    titles = []
    descriptions = []

    if requests.get(api_url).status_code == 200:
        while len(titles) < max:
            response = requests.get(api_url, params={"offset": offset})

            try:
                result = response.json()  # load json file
            except:
                continue
                
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


def get_ONS_datasets_urls():
    """
    Loads ONS api and loops through collecting their urls (that can be used to download a csv file of each one).
    
    As an example, the first url refers to the file that can be found online here:
    https://www.ons.gov.uk/datasets/wellbeing-quarterly/editions/time-series/versions/6
    """

    api_url = "https://api.beta.ons.gov.uk/v1/datasets"
    offset = 0
    max = 500
    datasets_urls = []

    while len(datasets_urls) < max:
        response = requests.get(api_url, params={"offset": offset})

        try:
            result = response.json()
        except:
            continue

        r = result['items']
        for row in r:
            edition = row.get("links").get("latest_version").get("href")
            datasets_urls.append(edition)

        offset += result['count']  # offset to avoid datasets already seen

        if result['count'] == 0:
            break

    return datasets_urls


def find_ONS_cols(url):
    "Finding the csv download link for a specific dataset."
    r = requests.get(url)

    if r.status_code == 200:
        test = r.json()
    
        if test.get('downloads'):
            temp_url = test.get("downloads").get("csv").get("href")
    
            # Has to be done like this to avoid HTTP 403 Error
            # Solution found at: https://datascience.stackexchange.com/questions/49751/read-csv-file-directly-from-url-how-to-fix-a-403-forbidden-error
            csv_url = requests.get(temp_url).text
            temp_df = pd.read_csv(StringIO(csv_url), dtype='string', on_bad_lines='skip')
            col_headings = temp_df.columns
            col_headings = col_headings.to_list()
        else:
            col_headings = float('nan')  # This means the link did not have a csv file href
    else:
        col_headings = float('nan')

    return col_headings


def get_ONS_long_description():
    """
    Getting a long description from the Quality and Methodology (QMI) page
    for all datasets available via the ONS api.
    """
    api_url = "https://api.beta.ons.gov.uk/v1/datasets"
    description_L = []
    MAX_RETRIES = 100

    for i in range(MAX_RETRIES):
        try:
            # Getting the qmi (Quality and Methodology Information) url
            response = requests.get(api_url, params={"limit": 1000})
            items = response.json()['items']
            break
        except:
            continue

    
    i = 0
    for item in items:

        try:
            qmi_url = item['qmi']['href']

            # Reading the HTML from the page
            response2 = requests.get(qmi_url).text
            soup = BeautifulSoup(response2, 'html.parser')

            """
            Searching for all text content in <p> elements. Removing any elements 
            contained within the <p> elements. Removing strings longer than 35 
            characters (to try get only descriptive content) and cleaning the content
            by removing \n and ' characters as well as any double spaces and the 
            square brackets surrounding each string.
            """
            temp_desc = ''
            for text in soup('p')[4:-7]:
                if text.contents != '':
                    x = str(text.contents)
                    y = re.sub("\<.*?\>", "", str(x))
                    y = re.sub(r"\s+", " ", y)
                    y = y.replace('\\n', '').replace('\'', '').replace(',', '')\
                    .replace('  ', ' ').replace('\\xa0', ' ')
                    if len(y) > 35:
                        temp_desc = temp_desc + y[1:len(y)-1]
        except:
            description_L.append('')
            continue

        description_L.append(temp_desc)

    return description_L


def find_ONS_cols_and_unique_vals(url):
    """
    Using the url provided this function:
    - Checks a download is possible
    - Downloads the csv file of the dataset
    - Gets all the column titles
    - Gets the unique values from columns containing non-numeric data

    Check is string contains number:https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-represents-a-number-float-or-int
    """

    temp = requests.get(url)
    try:
        temp = temp.json()
    except:
        return {}

    if temp['downloads']:
        temp_url = temp['downloads']['csv']['href']

        csv_url = requests.get(temp_url).text
        temp_df = pd.read_csv(StringIO(csv_url), low_memory=False)

        col_data = {}

        for col in temp_df.columns:
            col_data[col] = None

            if type(temp_df.loc[:, col][0]) == str: # Check for string data type
                if not temp_df.loc[:, col][0].replace('.','', 1).isdigit(): # if the data is a string ensure that it isn't numeric
                    col_data[col] = list(temp_df.loc[:, col].unique())
    else:
        col_data = {}   # This means the link didn't have a csv file href

    return col_data


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


