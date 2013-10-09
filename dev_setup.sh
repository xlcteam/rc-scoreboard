#!/bin/bash

echo "scoreBoard dev setup"
echo
echo "Step 1: installing Python requirements"
pip install -r requirements.txt

echo "Step 2: putting static items into static directory"
./manage.py collectstatic

echo "Step 3: setting up the DB"
./manage.py syncdb
./manage.py migrate soccer 
./manage.py migrate rescue 

echo "And you are ready to use scoreboard by running"
echo
echo "./manage.py runserver"
echo
echo "You can then access scoreBoard at http://127.0.0.1:8000"
