from flask import Flask, request
from flask import json
from flask.json import jsonify, load
from numpy import character
from sqlalchemy.util.langhelpers import method_is_overridden
import src.sql_tools as sql

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Hola Mundo"

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


app.run(debug=True)