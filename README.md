# dictionaryDB
bing dictionary SQLite3 DB. Used in aiBook

## python requirement
bs4==0.0.1

Django==3.1.4

## python script
python manage.py migrate

python manage.py makemigrations wikdictionary

python manage.py sqlmigrate wikdictionary 0001

python manage.py migrate

