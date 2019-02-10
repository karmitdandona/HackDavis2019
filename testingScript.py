import requests
import time
import twilioAuth

# URL = "http://localhost:5000"
URL = "https://calcium-scholar-231323.appspot.com"

s = requests.Session()

r = s.post(URL + "/login", data={"name": "Caller"})

cookies = r.cookies

r = s.post(URL + "/reminders", data={"info": "Check on Grandma Louise", "time": time.time() + 40}, cookies=cookies)

r = s.get(URL + "/reminders")

data = r.json()["reminders"]

# reminderToUpdate = {}
# for reminderDict in data:
#     if reminderDict["info"] == "Take medication":
#         reminderToUpdate = reminderDict
#         break

# reminderToUpdate['callee'] = twilioAuth.participant1
# r = s.post(URL + "/update_reminder", data=reminderDict, cookies=cookies)
