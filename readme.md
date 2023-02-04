# install pipenv (virtual environment)
### install pipx (isolates python packages)
`python3 -m pip install --user pipx`
### install pipenv with pipx (install pipenv in a isolated python environment)
`sudo apt install python3.10-venv`

`pipx install pipenv`

# install pipenv requirements
go to the project directory (where the Pipfile is located) and run:

`pipenv install`

# install redis
`sudo apt install redis-server`
### check if redis is running
### for checking if redis is running, open a new terminal and run:
`redis-cli`
### if redis is running you should see PONG after running:
`ping`
### for exiting redis-cli run:
`exit`

# run the project
### run django-q
`python3 manage.py qcluster`
### run django server
`python3 manage.py runserver`

# django-q monitors
### for checking the status of the django-q cluster run:
`python3 manage.py qmonitor`
### for checking the status of the django-q cluster run:
`python3 manage.py qinfo`
### for checking the status of the django-q cluster run:
`python manage.py qmemory`


