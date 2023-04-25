# ONS API scraper

Aims:
- Access the ONS API
- Create a list containing the titles of all available datasets through the api
- Get a short description of each
- Get the column titles of each dataset
- Provide a url which can be used to get further info about each dataset

## File Overviews

### ONS_scraper_functions.py

This file contains the functions: 
- get_ONS_datasets_titles_descriptions() which returns two lists; one containing the titles of each dataset and the other a description.
- get_ONS_datasets_urls() which returns a list of urls which can then be used to download every dataset.
- find_ONS_cols() which returns a list containing lists of the column titles for each dataset.
- get_nomis_datasets_titles_descriptions() which does the same as get_ONS_datasets_titles_descriptions() but uses the Nomis API (also worth noting this isn't used in the ONS_dataset_compendium.py file.

### ONS_dataset_compendium.py

This file runs each of the relevant functions from ONS_scraper_functions.py stores all information to a dataframe and saves to a csv. (Can take a while to run depending on internet speed).

### ONS_datasets_metadata.csv

This is simply the output of ONS_dataset_compendium.py containing the combined output of all the functions (excluding get_nomis_datasets_titles_descriptions().

### ONS_data_download_and_view.ipynb

A jupyter notebook that walks through the use of each of the ONS functions from ONS_scraper_functions.py. This includes a brief description of what each function does, how to use them, what inputs they need, and what they return. It also includes visualisation of the data in the form of dataframes and an example bar chart.
