# TaskMaster-API Documentation

## Introduction
The TaskMaster API allows you to manage tasks, including creating tasks, retrieving task details, managing subtasks, and editing tasks as collaborators.

## Base URL
```
https://taskmaster-api-9nna.onrender.com/api/
```

## Authentication

### Registration
To use the API, you must first register an account. Send a POST request with your username and password. Email is optional.

**Endpoint**: `POST /register/`

**Request Body**:
| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| username  | string | Required. Your username. |
| password  | string | Required. Your password. |
| email     | string | Optional. Your email.    |

**Example Request**:
```python
# With email
requests.post("https://taskmaster-api-9nna.onrender.com/api/register/", json={"email": "luigi@gmail.com", "username": "luigi", "password": "your_password"})

# Without email
requests.post("https://taskmaster-api-9nna.onrender.com/api/register/", json={"username": "luigi", "password": "your_password"})
```

**Example Response**:
```json
{
    "user": {
        "email": "luigi@gmail.com",
        "username": "luigi"
    },
    "token": "45d558b21488e65d2df01196820f491be"
}
```

### Requesting an Authentication Token
After registering, request an authentication token using your username and password.

**Endpoint**: `POST /api/auth/`

**Request Body**:
| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| username  | string | Required. Your username. |
| password  | string | Required. Your password. |

**Example Request**:
```python
requests.post("https://taskmaster-api-9nna.onrender.com/api/auth/", json={"username": "luigi", "password": "your_password"})
```

**Example Response**:
```json
{
    "token": "45d558b21488e65d2df0172adbad196820f491be"
}
```

### Authentication Header
Include your API token in the request header for authenticated endpoints:
```
Authorization: Token YOUR_API_TOKEN
```

## Endpoints

### Create Task
Create a new task with optional subtasks.

**Endpoint**: `POST /api/task/`

**Request Body**:
| Parameter      | Type     | Description                                              |
|----------------|----------|----------------------------------------------------------|
| title          | string   | Required. Title of the task.                             |
| status         | string   | Required. Status of the task (to-do, in-progress, completed). |
| due_date       | string   | Optional. Due date of the task (YYYY-MM-DD format).      |
| collaborators  | list     | Optional. List of collaborators (usernames) for the task.|
| subtasks       | list     | Optional. List of subtasks.                              |

**Example Request**:
```python
import requests

url = "https://taskmaster-api-9nna.onrender.com/api/task/"

headers = {
    "Authorization": "Token 45d558b21488e65d2df0172adbad196820f491be",
    "Content-Type": "application/json"
}

task = {
    "title": "Code Usability Task",
    "status": "in-progress",
    "due_date": "2024-06-23",
    "collaborators": ["johndoe"],
    "subtasks": [
        {
            "title": "Check Virality",
            "status": "to-do",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        },
        {
            "title": "Check Vulnerability",
            "status": "in-progress",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        },
        {
            "title": "Revamp Completed Tasks",
            "status": "in-progress",
            "due_date": "2024-06-23",
            "assigned_to": "luigi"
        }
    ],
    "task_owner": "luigi"
}

response = requests.post(url, json=task, headers=headers)
```

**Example Response**:
```json
{
    "id": 83,
    "title": "Code Usability Task",
    "status": "in-progress",
    "due_date": "2024-06-23",
    "collaborators": ["johndoe"],
    "task_owner": "luigi",
    "subtasks": [
        {
            "id": 117,
            "title": "Check Virality",
            "status": "to-do",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        },
        {
            "id": 118,
            "title": "Check Vulnerability",
            "status": "in-progress",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        },
        {
            "id": 119,
            "title": "Revamp Completed Tasks",
            "status": "in-progress",
            "due_date": "2024-06-23",
            "assigned_to": "luigi"
        }
    ]
}
```

### Get Single Task
Retrieve details of a single task by its ID.

**Endpoint**: `GET /api/task/{task_id}/`

**URL Parameters**:
| Parameter | Type    | Description              |
|-----------|---------|--------------------------|
| task_id   | integer | Required. ID of the task.|

**Request Headers**:
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Token YOUR_API_TOKEN  |

**Example Request**:
```python
import requests

url = "https://taskmaster-api-9nna.onrender.com/api/task/1/"

headers = {
    "Authorization": "Token 45d558b21488e65d2df0172adbad196820f491be"
}

response = requests.get(url, headers=headers)
```

**Example Response**:
```json
{
    "id": 1,
    "title": "Code Usability Task",
    "status": "in-progress",
    "due_date": "2024-06-23",
    "collaborators": ["johndoe"],
    "task_owner": "luigi",
    "subtasks": [
        {
            "id": 117,
            "title": "Check Virality",
            "status": "to-do",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        },
        // More subtasks
    ]
}
```

### Get All Tasks by User
Retrieve all tasks created by the authenticated user.

**Endpoint**: `GET /api/task/`

**Request Headers**:
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Token YOUR_API_TOKEN  |

**Example Request**:
```python
import requests

url = "https://taskmaster-api-9nna.onrender.com/api/task/"

headers = {
    "Authorization": "Token 45d558b21488e65d2df0172adbad196820f491be"
}

response = requests.get(url, headers=headers)
```

**Example Response**:
```json
[
    {
        "id": 1,
        "title": "Code Usability Task",
        "status": "in-progress",
        "due_date": "2024-06-23",
        "collaborators": ["johndoe"],
        "task_owner": "luigi",
        "subtasks": [
            {
                "id": 117,
                "title": "Check Virality",
                "status": "to-do",
                "due_date": "2024-06-23",
                "assigned_to": "johndoe"
            },
            // More subtasks
        ]
    },
    // More tasks
]
```

### View Collaborator Tasks
Retrieve all tasks in which the authenticated user is a collaborator.

**Endpoint**: `GET /api/task/collab/`

**Request Headers**:
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Token YOUR_API_TOKEN  |

**Example Request**:
```python
import requests

url = "https://taskmaster-api-9nna.onrender.com/api/task/collab/"

headers = {
    "Authorization": "Token 45d558b21488e65d2df0172adbad196820f491be"
}

response = requests.get(url, headers=headers)
```

**Example Response**:
```json
[
    {
        "id": 1,
        "title": "Code Usability Task",
        "status": "in-progress",
        "due_date": "2024-06-23",
        "task_owner": "luigi",
        "subtasks": [
            {
                "id": 117,
                "title": "Check Virality",
                "status": "to-do",
                "due_date": "2024-06-23",
                "assigned_to": "johndoe"
            },
            // More subtasks
        ]
    },
    // More tasks
]
```

### View Collaborator Task
Retrieve details of a specific

 task in which the authenticated user is a collaborator.

**Endpoint**: `GET /api/task/collab/{task_id}/`

**URL Parameters**:
| Parameter | Type    | Description              |
|-----------|---------|--------------------------|
| task_id   | integer | Required. ID of the task.|

**Request Headers**:
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Token YOUR_API_TOKEN  |

**Example Request**:
```python
import requests

url = "https://taskmaster-api-9nna.onrender.com/api/task/collab/1/"

headers = {
    "Authorization": "Token 45d558b21488e65d2df0172adbad196820f491be"
}

response = requests.get(url, headers=headers)
```

**Example Response**:
```json
{
    "id": 1,
    "title": "Code Usability Task",
    "status": "in-progress",
    "due_date": "2024-06-23",
    "task_owner": "luigi",
    "subtasks": [
        {
            "id": 117,
            "title": "Check Virality",
            "status": "to-do",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        },
        // More subtasks
    ]
}
```

### Edit Collaborator Task
Edit the status of a specific subtask in a task in which the authenticated user is a collaborator.

**Endpoint**: `PUT /api/task/collab/{task_id}/`

**URL Parameters**:
| Parameter | Type    | Description              |
|-----------|---------|--------------------------|
| task_id   | integer | Required. ID of the task.|

**Request Headers**:
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Token YOUR_API_TOKEN  |
| Content-Type  | string | application/json      |

**Request Body**:
| Parameter | Type    | Description                                              |
|-----------|---------|----------------------------------------------------------|
| subtasks  | list    | Required. List of subtasks to be modified.               |
| id        | integer | Required. ID of the subtask to be modified.              |
| status    | string  | Required. New status of the subtask (to-do, in-progress, completed). |

**Example Request**:
```python
import requests

url = "https://taskmaster-api-9nna.onrender.com/api/task/collab/1/"

headers = {
    "Authorization": "Token 45d558b21488e65d2df0172adbad196820f491be",
    "Content-Type": "application/json"
}

task = {
    "subtasks": [
        {
            "id": 117,
            "status": "in-progress"
        }
    ]
}

response = requests.put(url, json=task, headers=headers)
```

**Example Response**:
```json
{
    "id": 1,
    "title": "Code Usability Task",
    "status": "in-progress",
    "due_date": "2024-06-23",
    "task_owner": "luigi",
    "subtasks": [
        {
            "id": 117,
            "title": "Check Virality",
            "status": "in-progress",
            "due_date": "2024-06-23",
            "assigned_to": "johndoe"
        },
        // More subtasks
    ]
}
```

## Notes
- The `collaborators` field is a list of usernames of collaborators working on the task.
- The `subtasks` field is a list of subtasks that can be assigned to collaborators by the `task_owner`.
- The `status` field accepts only one of three parameters: `to-do`, `in-progress`, or `completed`.
- The `task_owner` field is the username of the user who created the task.
