import numpy as np
import pandas as pd
import os
import re


def import_kaggle_data(url):
    """
    It downloads a selected dataset from Kaggle and convers it to
    a pandas dataframe

   Args:
       kaggle url
       Input argument - Ask for the file you want to keep 
       from the unzip kaggle file, moves it to a folder named "data"
       and deletes the rest of non-needed downloaded files.

   Returns:
       kaggle csv file in data folder

    """

    #Download Kaggle dataset
    os.system(f'kaggle datasets download -d {url}')

    #Decompress zip file
    os.system('tar -xzvf *.zip')

    #List files in folder
    os.system('ls')

    # Select the file you want to keep
    selected_file = input('enter name of the file you want to keep:')

    # Move selected file to the data folder
    os.system(f'mv {selected_file} ../data')

    # Dump the rest of the files except jupyter notebooks
    # os.system('find . \! -name "*.ipynb" -delete')
    # os.system('rm !(*.ipynb)')
    os.system('ls -1 | grep -v "*.ipynb" | xargs rm -f')


    # Import csv to dataframe
    # df = pd.read_csv(f"../data/{selected_file}")

    # return df


def clean_characters(list_, database_name, column):
    """
    Removes list of unwanted character from a chosen column in a dataset

   Args:
       list of characters
       database name
       database column name

   Returns:
       nothing

    """
    for ch in list_:
        database_name[f'{column}'] = database_name[f'{column}'].str.replace(f"{ch}","")