import requests
import time
import twilioAuth

# URL = "http://localhost:5000"
URL = "https://calcium-scholar-231323.appspot.com"

s = requests.Session()

r = s.post(URL + "/login", data={"name": "Caller"})

cookies = r.cookies

r = s.post(URL + "/reminders", data={"info": "Take medication 4abc", "time": time.time() + 500}, cookies=cookies)

r = s.get(URL + "/reminders")

# data = r.json()["reminders"]

# reminderToUpdate = {}
# for reminderDict in data:
#     if reminderDict["info"] == "blah!":
#         reminderToUpdate = reminderDict
#         break

# print(reminderToUpdate)

# reminderToUpdate['callee'] = twilioAuth.participant1
# r = s.post(URL + "/update_reminder", data=reminderToUpdate, cookies=cookies)
