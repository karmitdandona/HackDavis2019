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

@app.route("/logout", methods=['GET'])
def logout():
  session.pop("name")
  session.pop("twilioID")
  return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
  # assign session vars: name, TwilioID
  data = request.form.to_dict()

  if data["name"] == "Caller":
    session["name"] = "John"
    session["twilioID"] = twilioAuth.participant0
  else:
    session["name"] = "Alice"
    session["twilioID"] = twilioAuth.participant1
  return redirect(url_for('success'))

def create_reminder(data):
    callee = data['callee']
    info = data['info']
    time = data['time']
    new_reminder = {
        "callee": callee,
        "caller": -1,
        "info": info,
        "time": time
    }
    reminders_collection.add(new_reminder)

def valid_reminder_data(data):
    return data['callee'] and data['info'] and data['time']

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
            all_reminders[i]['time'] = time.timestamp()
        all_reminders_dict = {"reminders": all_reminders}
        return json_create(all_reminders_dict)

@app.route("/update_reminder", methods=['POST'])
def update_reminder():
  """Overwrites a reminder with provided json (for when caller is updated)"""
  data = request.form.to_dict()

  if not valid_reminder_data(data):
    return redirect(url_for('failure'))

  reminders_collection.document(data['id']).set(data)

  timeToReminder = time.time() - data['time']
  calleeName = session['name']

  sendCallMessageArguments = [data['callee'], calleeName, data['reminder']]
  timer = threading.Timer(timeToReminder, twilioApiCalls.SendCallMessage, sendCallMessageArguments)

  return redirect(url_for('success'))
