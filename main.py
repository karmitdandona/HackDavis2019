from flask import Flask
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()
reminders = db.collection(u'reminders')

@app.route("/")
def index():
    return "Hello World!"

@app.route("/reminders")
def reminders():
    return "reminders"