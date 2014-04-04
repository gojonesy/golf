#!/bin/bash
# run through the process of adding all changes to git, committing and then sending # to heroku
# USAGE = autopush commit message

msg=$1

if [[ $msg == "" ]]; then
	msg="Auto_Push"
fi

git add .
git commit -m $msg
git push heroku master

# apply migrations
heroku run python manage.py migrate golf
