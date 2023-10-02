"""
Collecting and combining all dataset info into one place using the functions 
from ONS_scaper_functions.py and saving to as a csv

Author: Rowan Trickett
Date: 19/04/2023
Last updated: 24/04/2023
"""

from ONS_scraper_functions import *
import pandas as pd


""" ONS Data """

# Can take a long time to run depending on internet speed
titles, descriptions = get_ONS_datasets_titles_descriptions()
urls = get_ONS_datasets_urls()
long_desc = get_ONS_long_description()

latest_release = []
cols = []
col_data = []
count = 0

for url in urls:
    response = requests.get(url)
    try: 
        latest_release.append(response.json()['release_date'])
    except:
        latest_release.append(float('nan'))

    try:
        cols.append(find_ONS_cols(url))
    except:
        cols.append('')

    try:
        col_data.append(find_ONS_cols_and_unique_vals(url))
    except:
        col_data.append('')

    
    count +=1

ONS_df = pd.DataFrame({'Title': titles, 'Description': descriptions, 
                        'Long_description': long_desc, 'Columns': cols, 
                        'Unique_parameters': col_data, 'Latest_release': latest_release})

ONS_df.to_csv('ONS_datasets_metadata.csv')
