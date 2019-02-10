from flask import redirect
from flask import url_for
from flask import request
from flask import Flask
from google.cloud import firestore
from json import loads as json_load
from json import dumps as json_create
from datetime import datetime

app = Flask(__name__)

db = firestore.Client()
reminders_collection = db.collection(u'reminders')

@app.route("/")
def index():
    return "Hello World!"

@app.route("/success")
def success():
    return "{\"success\": true}"

@app.route("/failure")
def failure():
    return "{\"success\": false}"

def create_reminder(data):
    caller = data['caller']
    info = data['info']
    time = data['time']
    new_reminder = {
        "caller": caller,
        "callee": -1,
        "info": info,
        "time": time
    }
    reminders_collection.add(new_reminder)

def valid_reminder_data(data):
    return data['caller'] and data['info'] and data['time']

@app.route("/reminders", methods=['POST', 'GET'])
def reminders():
    if request.method == 'POST':
        data = request.form.to_dict()

        if not valid_reminder_data(data):
            return redirect(url_for('failure'))

        create_reminder(data)
        return redirect(url_for('success'))

    if request.method == 'GET':
        all_reminders = reminders_collection.get()
        all_reminders = [reminder.to_dict() for reminder in all_reminders]
        for i in range(len(all_reminders)):
            time = all_reminders[i]['time']
            all_reminders[i]['time'] = time.timestamp()
        all_reminders_dict = {"reminders": all_reminders}
        return json_create(all_reminders_dict)