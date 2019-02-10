import requests
import time

URL = ""

r = requests.post(URL + "/login", json={"name": "Caller"})

r = requests.post(URL + "/reminders", json={"info": "Take medication", "time": time.time() + 20})

r = requests.get(URL + "/reminders")

data = r.json()["reminders"]

reminderToUpdate = {}
for reminderDict in data:
  if reminderDict["info" == "Take medication"]:
    reminderToUpdate = reminderDict

r = requests.post(URL + "/update_reminder", json=reminderDict)
