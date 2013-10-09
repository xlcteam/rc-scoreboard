#!/bin/bash
pip install -r requirements.txt
./manage.py collectstatic
./manage.py syncdb
./manage.py migrate soccer 
./manage.py migrate rescue 
