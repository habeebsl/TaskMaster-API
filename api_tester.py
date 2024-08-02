import requests
import json

username = input("Enter Username: ")

if not username:
    username = "staff"

auth_token = requests.post("https://taskmaster-api-9nna.onrender.com/api/auth/", json={"username":username, "password":"Habeeb24434@"})

print(auth_token.text)

url = "https://taskmaster-api-9nna.onrender.com/api/task/"

headers = {
    "Authorization": f"Token {json.loads(auth_token.text).get('token')}",
    "Content-Type": "application/json"
}

task = {
    "title": "T 123",
    "status": "to-do",
    "collaborators": ["tobi"],
}

response = requests.get(url, json=task, headers=headers)

print(response.text)