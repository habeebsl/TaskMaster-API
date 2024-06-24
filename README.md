# TaskMaster-API

## Introduction
This API allows you to manage tasks, including creating tasks, retrieving task details, managing subtasks, and editing tasks as collaborators.

## Base URL
The base URL for all API requests.
```
https://api.example.com/v1
```

## Authentication
To use the API, you must first register and then obtain an authentication token.

### Registration
To register, send a POST request with your username and password. Email is optional.

#### HTTP Request
```
POST /register/
```

#### Request Body
| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| username  | string | Required. Your username. |
| password  | string | Required. Your password. |
| email     | string | Optional. Your email.    |

#### Example Request (with email)
```python
requests.post("http://127.0.0.1:8000/register/", json={"email": "luigi@gmail.com", "username": "luigi", "password": "your_password"})
```

#### Example Request (without email)
```python
requests.post("http://127.0.0.1:8000/register/", json={"username": "luigi", "password": "your_password"})
```

#### Example Response
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
After registration, request an authentication token using your username and password.

#### HTTP Request
```
POST /api/task/auth/
```

#### Request Body
| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| username  | string | Required. Your username. |
| password  | string | Required. Your password. |

#### Example Request
```python
requests.post("http://127.0.0.1:8000/api/task/auth/", json={"username": "luigi", "password": "your_password"})
```

#### Example Response
```json
{
    "token": "45d558b21488e65d2df0172adbad196820f491be"
}
```

### Authentication
Include your API token in the request header for authenticated endpoints:
```
Authorization: Bearer YOUR_API_TOKEN
```

## Endpoints

### Create Task
Create a new task with optional subtasks.

#### HTTP Request
```
POST /api/task/
```

#### Request Body
| Parameter      | Type     | Description                                              |
|----------------|----------|----------------------------------------------------------|
| title          | string   | Required. Title of the task.                              |
| status         | string   | Required. Status of the task (to-do, in-progress, completed). |
| due_date       | string   | Required. Due date of the task (YYYY-MM-DD format).       |
| collaborators  | list     | Optional. List of collaborators (usernames) for the task.|
| subtasks       | list     | Optional. List of subtasks.                               |
| task_owner     | string   | The user (username) who created the task.                 |

#### Example Request (with subtasks)
```python
url = "http://127.0.0.1:8000/api/task/"

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

#### Example Response
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

#### HTTP Request
```
GET /api/task/{task_id}/
```

#### URL Parameters
| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| task_id   | integer| Required. ID of the task.|

#### Request Headers
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Bearer YOUR_API_KEY  |

#### Example Request
```
GET http://127.0.0.1:8000/api/task/1/
Authorization: Bearer YOUR_API_KEY
```

#### Example Response
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

#### HTTP Request
```
GET /api/task/
```

#### Request Headers
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Bearer YOUR_API_KEY  |

#### Example Request
```
GET http://127.0.0.1:8000/api/task/
Authorization: Bearer YOUR_API_KEY
```

#### Example Response
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

#### HTTP Request
```
GET /api/task/collab/
```

#### Request Headers
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Bearer YOUR_API_KEY  |

#### Example Request
```
GET http://127.0.0.1:8000/api/task/collab/
Authorization: Bearer YOUR_API_KEY
```

#### Example Response
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
Retrieve details of a specific task in which the authenticated user is a collaborator.

#### HTTP Request
```
GET /api/task/collab/{task_id}/
```

#### URL Parameters
| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| task

_id   | integer| Required. ID of the task.|

#### Request Headers
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Bearer YOUR_API_KEY  |

#### Example Request
```
GET http://127.0.0.1:8000/api/task/collab/1/
Authorization: Bearer YOUR_API_KEY
```

#### Example Response
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

#### HTTP Request
```
PUT /api/task/collab/{task_id}/
```

#### URL Parameters
| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| task_id   | integer| Required. ID of the task.|

#### Request Headers
| Header        | Type   | Description          |
|---------------|--------|----------------------|
| Authorization | string | Bearer YOUR_API_KEY  |
| Content-Type  | string | Required. Set to "application/json". |

#### Request Body
| Parameter | Type   | Description                                              |
|-----------|--------|----------------------------------------------------------|
| subtasks  | list   | Required. List of subtasks to be modified.               |
| id        | integer| Required. ID of the subtask to be modified.              |
| status    | string | Required. New status of the subtask (to-do, in-progress, completed). |

#### Example Request
```python
url = "http://127.0.0.1:8000/api/task/collab/1/"

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

#### Example Response
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

---
