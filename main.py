from flask import Flask, request
from flask import json
from flask.json import jsonify, load
from numpy import character
from sqlalchemy.util.langhelpers import method_is_overridden
import src.sql_tools as sql
import markdown.extensions.fenced_code

app = Flask(__name__)


@app.route('/')
def index():
    readme_file = open("Doc.md", "r")
    md_template = markdown.markdown(readme_file.read(), extensions = ["fenced_code"])
    return md_template

@app.route("/sentences/")
def allsentence():
    sentences = sql.all_sentences()
    return sentences


@app.route("/sentences/<speaker>")
def speakersentence(speaker):
    print(speaker)
    sentences = sql.speaker_sentence(speaker)
    return sentences


@app.route("/newsentence", methods=["POST"])
def newsentence():
    data = dict(request.form.to_dict())

    try:
        resp = sql.insert_register(data)
        print(f"respuesta sql: {resp}")

        return {"error": 0, "msg": resp} 
    
    except Exception as e:
        print(f"There has been an error: {e}")
        return {"error": 1, "msg": e} 


@app.route("/sentiment/")


def sentiment_pol():

    sentences = sql.get_polarity()
    return sentences


# @app.route("/polarity/<speaker>")

# def polarity(speaker):
    
#     sentences = sql.speaker_sentence(speaker)
#     return sentences

app.run(debug=True)