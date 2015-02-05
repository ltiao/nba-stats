from fabric.api import local, settings, lcd
from django.contrib.auth.models import User

def hello():
    print("Hello world!")

def flushmigrations():
	with settings(warn_only=True):
		local("rm nba_stats/nba/migrations/*")

def createdb(name):
	local("createdb {name}".format(**locals()))

def dropdb(name):
	with settings(warn_only=True):
		local("dropdb {name}".format(**locals()))

def makemigrations(app_label):
	with lcd("nba_stats"):
		local("python manage.py makemigrations {app_label}".format(**locals()))

def migrate():
	with lcd("nba_stats"):
		local("python manage.py migrate")

def createsuperuser():
	User.objects.create_superuser('admin', 'admin@example.com', 'admin')

def hardflush(db_name, app_label):
	dropdb(db_name)
	flushmigrations()
	makemigrations(app_label)
	createdb(db_name)
	migrate()
	createsuperuser()