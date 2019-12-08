# AppFisher

Project : Fisher
Requirement : Python3

## Steps to install and run project

clone from repository

Before You Begin
> `sudo apt update`

Install Python Virtualenv
> `sudo apt install virtualenv`

create virtual environment:
> `virtualenv -p python3 venv`

activate environment
> `source venv/bin/activate`

define database in mysql
> database name `fisher_db`

move to project root directory
> `cd fisher-python`

install required packages
> `pip install -r requirements.txt`

after connection to database do migrations
> `python manage.py makemigrations`
> `python manage.py migrate`

to create super user
> `python manage.py createsuperuser`

run project
> `python manage.py runserver`

