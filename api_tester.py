import requests
import json

username = input("Enter Username: ")

if not username:
    username = "staff"

auth_token = requests.post("http://127.0.0.1:8000/api/task/auth/", json={"username":username, "password":"Habeeb24434@"})

url = "http://127.0.0.1:8000/api/task/collab/83/"

headers = {
    "Authorization": f"Token {json.loads(auth_token.text)['token']}",
    "Content-Type": "application/json"
}

data = {
    "subtasks": [
        {
        "title": "Check Virality",
        "status": "in-progress",
        "assigned_to": "staff"
        },

        {
        "id": 118,
        "title": "Check Vulnerability",
        "status": "in-progress",
        "assigned_to": "habeeb"
        }
    ],

    "collaborators": ['habeeb', 'staff']
}


response = requests.put(url, data=json.dumps(data), headers=headers)

print(response.text)