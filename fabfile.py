# The 'fabfile.py' is used by Fabric and must reside in the application root directory.

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from contextlib import contextmanager
from ibwt.startup.settings import LANGUAGES

@task
def update_env():
    """
    Install required Python packages using pip and requirements.txt
    """
    local('pip install -r requirements.txt')


@task
def reset_db():
    """
    Drop all tables, Create empty tables, and populate tables
    """
    local('PYTHONPATH=. python ibwt/startup/reset_db.py')


@task
def test():
    """
    Run the automated test suite using py.test
    """
    local('py.test --tb=short -s tests/')


@task
def test_cov():
    """
    Run the automated test suite using py.test
    """
    local('py.test --tb=short -s  --cov app  --cov-config tests/.coveragerc  --cov-report term-missing  tests/')


@task
def runserver():
    """
    Start the web application using a development WSGI webserver provided by Flask
    """
    local('python runserver.py')


@task
def deploy():
    """
    Deploy web application to Heroku.
    Requires: heroku git:remote -a PROJECTNAME
    """
    local('git push heroku master')


@task
def init_locales():
    with cd('/var/www/ibwtproject/ibwt'):
        #local('pybabel extract -F babel.cfg -o messages.pot .')
        for lang in LANGUAGES:
            local('pybabel init -i messages.pot -d translations -l %s' % lang)
            local('pybabel init -d translations -l %s -D flask_user -i flask_user.pot' % lang)
        local('pybabel compile -fd translations')
        local('pybabel compile -fd translations -fD flask_user')

@contextmanager
def virtualenv(venv_name):
    with prefix('source ~/.virtualenvs/'+venv_name+'/bin/activate'):
        yield