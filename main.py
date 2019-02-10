from flask import redirect
from flask import url_for
from flask import request
from flask import Flask
from flask import session
from google.cloud import firestore
from json import loads as json_load
from json import dumps as json_create
from datetime import datetime
import threading
import twilioApiCalls
import twilioAuth
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "HACKDAVIS"

db = firestore.Client()
reminders_collection = db.collection(u'reminders')

EMPTY_CALLER = -1

@app.route("/")
def index():
    return "Hello World!"

@app.route("/success")
def success():
    return "{\"success\": true}"

@app.route("/failure")
def failure():
    return "{\"success\": false}"

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop("name")
    session.pop("twilioID")
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    # assign session vars: name, TwilioID
    data = request.form.to_dict()
    print(data)
    if data["name"] == "Caller":
        session["name"] = "John"
        session["twilioID"] = twilioAuth.participant1
    else:
        session["name"] = "Mary"
        session["twilioID"] = twilioAuth.participant0
    print(session)
    return redirect(url_for('success'))

def create_reminder(data):
    callee = twilioAuth.participant1  # always KP40 (Mary)
    info = data['info']
    time = data['time']
    name = "Mary"  # should always be Mary, since Mary is always callee
    if type(time) == str:
        time = float(time)
    new_reminder = {
        "callee": callee,
        "name": name,
        "caller": EMPTY_CALLER,
        "info": info,
        "time": datetime.fromtimestamp(time)
    }
    reminders_collection.add(new_reminder)

def valid_reminder_data(data):
    print(session)
    # return session.get('twilioID', False) and data.get('info', False) and data.get('time', False)
    return data.get('info', False) and data.get('time', False)

def reminder_to_dict(reminder):
    id_ = reminder.id
    reminder_dict = reminder.to_dict()
    reminder_dict['id'] = id_
    return reminder_dict

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
        all_reminders = [reminder_to_dict(reminder) for reminder in all_reminders]
        all_reminders = [reminder for reminder in all_reminders if reminder['caller'] == -1]
        for i in range(len(all_reminders)):
            time = all_reminders[i]['time']
            if isinstance(time, datetime):
                all_reminders[i]['time'] = time.timestamp()
        all_reminders_dict = {"reminders": all_reminders}
        return json_create(all_reminders_dict)

@app.route("/update_reminder", methods=['POST'])
def update_reminder():
    """Overwrites a reminder with provided json (for when caller is updated)"""
    data = request.form.to_dict()

    if not valid_reminder_data(data):
        return redirect(url_for('failure'))

    data["caller"] = twilioAuth.participant1  # John (always the caller)

    reminders_collection.document(data['id']).set(data)

    timeToReminder = time.time() - float(data['time'])
    calleeName = data['name']  # (should always be Mary)
    
    twilioApiCalls.SendCallMessage(data['caller'], calleeName, data['info'])

    return redirect(url_for('success'))