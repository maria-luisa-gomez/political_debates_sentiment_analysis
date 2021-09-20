import numpy as np
import pandas as pd
import os
import re
import string
import en_core_web_sm
import spacy
from nltk.corpus import stopwords
from langdetect import detect
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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


def tokenizer(txt):
    """
     This function reads strings and gives back its tokenization

    Args:
     - 1 Detects language (en or es)
     - 2 It does lemmatisation to each word, removes spaces and stopword and lower cases

    Returns:
      string tokenize

    """

    try:
        if detect(txt) == 'en':
            nlp = spacy.load("en_core_web_sm")
        elif detect(txt) == 'es':
            nlp = spacy.load("es_core_news_sm")
        else:
            return "It's not English or Spanish"
            
    except:
        return "this can't be analize"
    
    
    tokens = nlp(txt)
    filtradas = []
    
    for word in tokens:
        if not word.is_stop:
            lemma = word.lemma_.lower().strip()
            if re.search('^[a-zA-Z]+$',lemma):
                filtradas.append(lemma)
            
    return " ".join(filtradas)


