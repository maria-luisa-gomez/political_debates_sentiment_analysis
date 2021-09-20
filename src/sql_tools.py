from config.configuration import engine
import pandas as pd



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
    Gets all data from political_debates mysql database

   Args:
   query from flask end point http://127.0.0.1:5000/sentences/

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

# validates keys allowed
def validate_keys_allowed(dict_):
    allowed_keys = ["speaker", "sentence", "minute", "debate"]
    for keys in allowed_keys:
        if keys in dict_:
            return True
        else:
            return False

# validates the number of keys needed
def validate_dict_len(dict_):
        allowed_keys = ["speaker", "sentence", "minute", "debate"]
        if len(dict_) == 4:
            return True
        else:
            print(f"Incorrect keys: These are the keys allowed and needed: {allowed_keys}")      


# validates keys allowed, needed and checks if key value is missing
def validate_keys(dict_):
    if validate_keys_allowed(dict_):
        if validate_dict_len(dict_):
            for k,v in dict_.items():
                if len(v) == 0:
                    print(f"The value of {k} is missing")
                else:
                    return True


# validates keys allowed, needed, checks if key value is missing, checks if "speaker" value already exists and if not inserts it into speakers table. It also gets speakersid needed for inserting new registers into peeches table

def insert_register(dict_):

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
                if len(sentence_query) > 0:
                    print(f"'{v}' is already in the database")
                    return f"'{v}' is already in the database"
                    

            else:
                
                pass
            
    #deletes "speaker" key and creates new key value "speakerid" needed to INSERT INTO speeches table            
    del dict_copy["speaker"]        
    dict_copy['speakerid'] = speakerid
    
    query_insert = f"""
    INSERT INTO speeches (minute, sentence, debate, speakers_speakerid)
    VALUES ("{dict_copy['minute']}","{dict_copy['sentence']}","{dict_copy['debate']}", {dict_copy['speakerid']});
    """
  
    print(query_insert)

    engine.execute(query_insert)


    return f"The register was uploaded successfully {dict_}"


# -----DEFENSIVE PROGRAMMING / ERROR HANDELING----END 


