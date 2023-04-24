"""
Collecting and combining all dataset info into one place using the functions 
from ONS_scaper_functions.py and saving to as a csv

Author: Rowan Trickett
Date: 19/04/2023
Last updated: 24/04/2023
"""

import ONS_scraper_functions as osf

import pandas as pd


"""Combining both API lists"""
titles, descriptions = osf.get_ONS_datasets_titles_descriptions()
titles_nomis, descriptions_nomis = osf.get_nomis_datasets_titles_descriptions()
ONS_dataset_titles = titles + titles_nomis
ONS_dataset_descriptions = descriptions + descriptions_nomis

urls = osf.get_ONS_datasets_urls()
url_df = pd.DataFrame({'URLs': urls})
url_df.to_csv('temp.csv')


"""
Produces a list of lists containing all column titles

Notes:
- Takes a long time so avoid running if you can
"""
column_titles = []
count = 0
for url in urls:
    column_titles.append(osf.find_ONS_cols(url))
    print(count)
    count += 1


# Combining all data into a dataframe and saving as a csv
ONS_df = pd.DataFrame({'Titles': titles, 'Column_Titles': column_titles, 'description': descriptions, 'URLs': urls})
ONS_df.to_csv('ONS_datasets_metadata.csv')


""" 
Comparing the dataset titles in the UK_metadata_compendium with the 
titles of datasets available from the ONS API 
"""
#UK_metadata_compendium = "/Users/slowz/Downloads/UK_metadata_compedium.csv"
#df = pd.read_csv(UK_metadata_compendium)
#print(df['Name'])
#print(df['Name'].isin(ONS_datasets).any())