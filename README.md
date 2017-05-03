### Testing task for Judolaunch co.
Created by me (Boris Paschenko), 3.05.2017

## Setup

`git clone https://github.com/dolferoIHYD/Judolaunch-test.git`
`cd Judolaunch-test`
`virtualenv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`
`python manage.py migrate`

## Running

`python manage.py runserver`
or
`python manage.py runserver <port>`
to run in non standart port


## Depends

virtualenv
python2.7
