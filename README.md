# Political Debates API

![portada](https://ichef.bbci.co.uk/news/640/cpsprodpb/EB25/production/_113979106_788cafdb-afda-4718-90f4-7212c3e16662.jpg)

### Objective

Create an API capable of making possible for the user to get information about political debates from a sql database and alter its content as well.
Developers can access information about what has been said by the politician during the debate and minute when that happened. It also provides with information about polarity score of each sentence said.


### METHODS

Mysql

Flask

GET and POST request

NLP


### STEPS

**1 - Kaggle data download, cleaning and Mysql upload.ipynb**: In this notebook we work on:

- Downloading kaggle source data. (import_kaggle_data function -> kaggle_data_functions.py)

- Giving the dataframe the appropiate format (clean_characters function -> kaggle_data_functions.py)

- Adding some columns needed like  "speakerid", "sentence id" and "tokens" (sentence said tokenized, tokenizer function-> kaggle_data_functions.py).

- Import dataframe to sql political_database (political_debate_database_squema.sql)


**2 - Get and Post API requests.ipynb**: API calls:

- GET requests: get endpoints -> main.py and query functions -> sql_tools.py

- POST request: post endpoints -> main.py and query and defensive programming functions -> sql_tools.py



**3 - NLP.ipynb**: sentiment analyis: 

- Stablishing conexion with the database -> configuariton.py

- Get endpoints  -> main.py and  query sentiment analysis -> functions sql_tools.py 



API Documentation ->[Doc.md](https://github.com/maria-luisa-gomez/political_debates_sentiment_analysis/blob/main/Doc.md)


## Libraries

[flask](https://flask.palletsprojects.com/en/2.0.x/)

[NLTK](https://www.nltk.org/api/nltk.sentiment.html)

[sqlalchemy](https://www.sqlalchemy.org)

[sys](https://docs.python.org/3/library/sys.html)

[requests](https://pypi.org/project/requests/2.7.0/)

[pandas](https://pandas.pydata.org/)

[dotenv](https://pypi.org/project/python-dotenv/)

[mysql](https://www.mysql.com)

[json](https://docs.python.org/3/library/json.html)

[os](https://docs.python.org/3/library/os.html)


[operator](https://docs.python.org/3/library/operator.html)


[re](https://docs.python.org/3/library/re.html)


