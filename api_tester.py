import requests
import json

username = input("Enter Username: ")

if not username:
    username = "staff"

auth_token = requests.post("http://127.0.0.1:8000/api/task/auth/", json={"username":username, "password":""})

print(auth_token.text)

url = "http://127.0.0.1:8000/api/task/collab/1/"

headers = {
    "Authorization": f"Token 45d558b21488e65d2df0172adbad196820f491be",
    "Content-Type": "application/json"
}

task = {
    "subtasks": [
        {
            "id": 117,
            "title": "Check Virality",
            "status": "to-do",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        }
    ]
}

response = requests.put(url, data=task, headers=headers)

# print(response.text)