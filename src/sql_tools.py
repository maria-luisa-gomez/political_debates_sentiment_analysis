from config.configuration import engine
import pandas as pd
import string
import en_core_web_sm
import spacy
from nltk.corpus import stopwords
from langdetect import detect
import re
from textblob import TextBlob
import nltk
# from googletrans import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer





def all_sentences():
    """
    Gets all data from political_debates mysql database

   Args:
   query from flask end point http://127.0.0.1:5000/sentences/

   Returns:
       json with query results

    """
    query = f"""
            SELECT * FROM speeches
            INNER JOIN speakers ON speeches.speakers_speakerid = speakers.speakerid
            """

    datos = pd.read_sql_query(query,engine)

    return datos.to_json(orient="records")




def speaker_sentence(speaker):
    """
    Gets all data from political_debates filtered by given speaker name

    Args:
    query from flask end point http://127.0.0.1:5000/sentences/<speaker>

   Returns:
       json with query results

    """
    query = f"""
            SELECT * FROM speeches
            INNER JOIN speakers ON speeches.speakers_speakerid = speakers.speakerid
            WHERE speaker = '{speaker}'"""

    datos = pd.read_sql_query(query,engine)

    return datos.to_json(orient="records")



# DEFENSIVE PROGRAMMING / ERROR HANDELING

# This is a secuence of smaller functions than handle bits of possible errors
# that will be part of a bigger function below named "insert_register"

# 1 function) validates keys allowed
def validate_keys_allowed(dict_):
    """
    Checks if needed keys for posting are in the dict provided by the
    api user

    Args:
        Read from a list of need keys and checks is they are in the dictionary
        provided by the user

    Returns:
       True or False

    """
    allowed_keys = ["speaker", "sentence", "minute", "debate"]
    for keys in allowed_keys:
        if keys in dict_:
            return True
        else:
            return False

# 2 function) validates the number of keys needed
def validate_dict_len(dict_):
    """
    Checks is the dictionary provided by the api user are the right number

    Args:
        Counts the number of keys in the dictionary and if it's different from
        needed, reminds the user which ones should be use

    Returns:
       True or False

    """
    
    allowed_keys = ["speaker", "sentence", "minute", "debate"]
    if len(dict_) == 4:
        return True
    else:
        print(f"Incorrect keys: These are the keys allowed and needed: {allowed_keys}")      


# 3 funcition) validates keys allowed, needed and checks if key value is missing
def validate_keys(dict_):
    """
    Validates keys allowed, needed and checks if key value is missing. 
    This function calls validate_keys_allowed and validate_dict_len functions.

    Args:
        validate_keys_allowed function runs, if True runs validate_dict_len,
        if True checks is there're keys with missing values

    Returns:
       True or False

    """
    if validate_keys_allowed(dict_):
        if validate_dict_len(dict_):
            for k,v in dict_.items():
                if len(v) == 0:
                    print(f"The value of {k} is missing")
                else:
                    return True


# validates keys allowed, needed, checks if key value is missing, checks if "speaker" value already exists and if not inserts it into speakers table. It also gets speakersid needed for inserting new registers into peeches table

def insert_register(dict_):
    """
     This function calls validate_keys_allowed, validate_dict_len and validare_keys to
     validates keys allowed, needed and checks if key value is missing. If dictionary has correct format
     checks speaker's id (needed for inserting new registers) and sentence duplicity

    Args:
        validate_keys_allowed function runs, if True
        -> runs validate_dict_len:
           -> if True, checks is there're keys with missing values
           -> if False it will return if there's a problem with the dictionary provided by the api user
        -> checks if speaker key value is already in political_database speakers table:
            if True -> sql queries for the speaker id
            if False -> adds speaker value to speakers table and get new speakerid autogenerate it by sql table
        -> checks id sentences value is not already the speeches table:
           - if True -> Returns a message to the user flagging that is already in the database
           - if False -> inserts new register to speaker and speeches sql tables

    Returns:
       Error messages (not valid dictionary) or successfull upload message

    """

    # makes a copy of the dictionary
    dict_copy = dict(dict_)

    
    if validate_keys(dict_copy):
        
        for k, v in dict_copy.items():
            
            if k == "speaker":
                speaker_query = list(engine.execute(f"SELECT speaker FROM speakers WHERE speaker = '{v}'"))
                if len(speaker_query) > 0:
                    speakerid = list(engine.execute(f"SELECT speakerid FROM speakers WHERE speaker ='{v}';"))[0][0]
                    

                else:
                    engine.execute(f"INSERT INTO speakers (speaker) VALUES ('{v}');")
                    speakerid = list(engine.execute(f"SELECT speakerid FROM speakers WHERE speaker ='{v}';"))[0][0]


            elif k == "sentence":
                sentence_query = list(engine.execute(f"SELECT sentence FROM speeches WHERE sentence = '{v}'"))
                
                print(dict_copy)
                if len(sentence_query) > 0:
                    print(f"'{v}' is already in the database")
                    return f"'{v}' is already in the database"
                    

            else:
                
                pass
            
    #deletes "speaker" key and creates new key value "speakerid" needed to INSERT INTO speeches table            
    del dict_copy["speaker"]        
    dict_copy['speakerid'] = speakerid
    dict_copy['tokens'] = tokenizer(dict_copy['sentence'])


    query_insert = f"""
    INSERT INTO speeches (minute, sentence, tokens, debate, speakers_speakerid)
    VALUES ("{dict_copy['minute']}","{dict_copy['sentence']}", "{dict_copy['tokens']}","{dict_copy['debate']}", {dict_copy['speakerid']});
    """
  
    print(query_insert)

    engine.execute(query_insert)


    return f"The register was uploaded successfully {dict_}"


# -----DEFENSIVE PROGRAMMING / ERROR HANDELING----END 


def sentiment(sentence):

    """
     This function reads strings (sentence) tokenized and gives back its polarity

    Args:
      
      Recieves a string (sentence) and applies compound score, this score 
      is computed by summing the valence scores of each word in the lexicon, 
      adjusted according to the rules, and then normalized to be between -1 
      (most extreme negative) and +1 (most extreme positive). 
      

    Returns:
      
      String(sentence) polarity

    """
    sia = SentimentIntensityAnalyzer()
    polaridad = sia.polarity_scores(sentence)
    pol = polaridad["compound"]
    return pol


def get_polarity():

    """
     This function gives back all the information within political_debates databates
     and calculates the polarity of each sentence said

    Args:
      
    query from flask end point http://127.0.0.1:5000/sentiment/
      

    Returns:
      
      json with query results with new object 'polarity'

    """

    df = pd.read_sql_query("""
    SELECT speaker, speakerid, minute, sentence, tokens, speakers_speakerid, debate FROM speeches
    INNER JOIN speakers ON speeches.speakers_speakerid = speakers.speakerid
     """, engine)
    
    df["polarity"] = df.tokens.apply(sentiment)

    return df.to_json(orient="records")


def get_speaker_polarity(speaker):
    """
    Gets all data from political_debates filtered by given speaker name

    Args:
    query from flask end point http://127.0.0.1:5000/sentiment/<speaker>

   Returns:
       json with query results adding calculate polarity parameter

    """
    query = f"""
            SELECT speaker, speakerid, minute, sentence, tokens, speakers_speakerid, debate FROM speeches
            INNER JOIN speakers ON speeches.speakers_speakerid = speakers.speakerid
            WHERE speaker = '{speaker}'"""

    df = pd.read_sql_query(query,engine)
    df["polarity"] = df.tokens.apply(sentiment)

    return df.to_json(orient="records")

