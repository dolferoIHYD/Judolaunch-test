## Testing task for Judolaunch co.
Created by me (Boris Paschenko), 3.05.2017

### Task

Build a task list application in django.
Users will first login to their accounts.
Once they login, then should see a list of everyone’s tasks.
There is an “Add” button to add a new todo item.
You can via the UI “Edit”, “Mark Done” or “Delete” a task.
Edit: Is editing the task name, description and status (done/undone) (only your own)
Mark Done: is changing the status of a task to “done” and record who did it.
Delete: is deleting a task (only your own)
There is a “Hide Completed tasks” button, click on that to filter out todo items that are already done.
Tests for the application. (We value good testing over complicated features)

### Setup

`git clone https://github.com/dolferoIHYD/Judolaunch-test.git` <br>
`cd Judolaunch-test` <br>
`virtualenv venv` <br>
`source venv/bin/activate` <br>
`pip install -r requirements.txt` <br>
`python manage.py migrate` <br>

### Running

`python manage.py runserver` <br>
or <br>
`python manage.py runserver <port>` <br>
to run in non standart port


### Depends

virtualenv
python2.7
