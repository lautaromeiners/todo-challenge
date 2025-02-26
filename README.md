# Invera ToDo-List Challenge (Python/Django Jr-SSr)

ToDo List API that allows users to register, login & perform CRUD and filtering operations over Tasks.

## Installation Instructions

After cloning the repository the first step for installation is creating a virtual environment.

```
python3.8 -m venv venv
```

And activate it

```
source venv/bin/activate
```

Once we've got the virtual environment activated we have to install the required dependencies. For this project I'm using pip, so the command to run is

```
pip install -r requirements.txt
```

With the dependencies installed, what's left to do is run migrations.

```
python manage.py migrate
```

With this step done we are ready to run our server.

```
python manage.py runserver
```

Or we can run the tests to make sure that everything works correctly

```
python manage.py test
```

## Usage Instructions

With the repo installed and ready to go, now we need to be able to use the application. We expose an API where a user can perform CRUD and filtering operations over Tasks.

The easiest way to use this, is with cURL.

The first thing we need to do is register

```
curl -X POST \
  http://localhost:8000/api/v1/auth/registration/ \
  -H 'Content-Type: application/json'   -d '{"username": "test", "email": "test@example.com", "password1": "secretpassword", "password2": "secretpassword"}'
```
Of course you can use whatever username, email and password you want. So once we get the token we will paste it in the header on subsequent API calls. All the other endpoints require authentication.

Here's a comprehensive list of actions you can perform

Create a Task

```
curl -X POST http://localhost:8000/api/v1/tasks/ \
     -H "Authorization: Token <your_token>" \
     -H "Content-Type: application/json" \
     -d '{ "title": "New Task", "description": "This is a description of the new task."}'
```

List Tasks

```
curl -X GET http://localhost:8000/api/v1/tasks/ \
     -H "Authorization: Token <your_token>"
```

Get Task details

```
curl -X GET http://localhost:8000/api/v1/tasks/<task_id>/ \
     -H "Authorization: Token <your_token>"
```

Update a Task

```
curl -X PATCH http://localhost:8000/api/v1/tasks/<task_id>/ \
     -H "Authorization: Token <your_token>" \
     -H "Content-Type: application/json" \
     -d '{ "status": 1 }'
```

Delete a Task

```
curl -X DELETE http://localhost:8000/api/v1/tasks/<task_id>/ \
     -H "Authorization: Token <your_token>"
```

We can also filter Tasks by title

```
curl -X GET "http://localhost:8000/api/v1/tasks/?title=Task" \
     -H "Authorization: Token <your_token>"
```

Or by status

```
curl -X GET "http://localhost:8000/api/v1/tasks/?completed=true" \
     -H "Authorization: Token <your_token>"
```

```  
curl -X GET "http://localhost:8000/api/v1/tasks/?completed=false" \
     -H "Authorization: Token <your_token>"
```

# Code Quality

Code is formatted with Black, DRF Viewsets are used to provide clear, readable code & to adhere to ReST best practices guaranteeing the appropiate HTTP methods are used. The application has unit & integration tests covering most of the application logic. Django's app structure is used to separate concerns from Authentication and Tasks, ensuring reusability. Third-party applications are used to provide robust, battle tested authentication & filtering. The User model extends AbstractUser ensuring flexibility and avoids potential migration issues later (as per Django's best practices). I decided to use a choices field for the status instead of a simple boolean field (such as completed) in order to adhere to Open/Closed SOLID principle, as the choices field allows you to easily add more statuses in the future without modifying the existing code. 
