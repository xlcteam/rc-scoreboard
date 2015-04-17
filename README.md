scoreBoard
==========

scoreBoard is a simple tool for displaying the score of any game.

The [original scoreBoard](https://github.com/xlcteam/scoreBoard-php) has been written in messy PHP.

## About rc-scoreboard

`rc-scoreboard` is a fork of scoreboard which is aiming at providing a fully
comprehensive solution for the RoboCup competition.

## Dependencies
The only real dependency is `python` (preferably cpython2.7) and [pip](http://www.pip-installer.org/en/latest/installing.html)  so that you
can install other dependencies (see requirements.txt).


## Setting up a development environment
* You need to create some virtual environment
* Then install all the dependencies by running `$ pip install -r requirements.txt` as
  superuser
* Then, to get all we need `$ python manage.py collectstatic`
* Now we shall sync the DB `$ python manage.py syncdb`
* Than we need to get migrations into the DB
    `$ python manage.py migrate soccer`
    `$ python manage.py migrate rescue`
* And in case we want to export results to PDF files, `wkhtmltopdf` has to be
  installed (the actual application, not the python wrapper)

Or just run the `dev_setup.sh` script.

### Server installation

* Install Python, PIP and GIT. Make sure the `libevent-dev` is also installed.
  You can easily installed by running `apt-get install libevent-dev` as root on
  Debian-like Linux servers.
* Clone this repository to a directory of your linking.
* Install all the dependencies by running `$ pip install -r requirements.txt`
  as superuser
* If you want to export results to PDF files, make sure the `wkhtmltopdf`
  executable is present at the server.


### Deployment

* Set `DEBUG` in `settings.py` to False
* Start nginx by running `nginx -c ./nginx.conf -p $PWD` in `./conf/`
* Run `python2 ./manage.py run_gunicorn`

*Note*: This application is still in the alpha version and not meant for actual use. Please [contact us](http://xlc-team.info/contact) if you plan on using it.

## Tests

You can run the tests by executing

    $ ./manage.py test scorebrd
    $ ./manage.py test soccer
    $ ./manage.py test rescue
    $ ./manage.py test rescueB


We really appreciate feedback, so if you have any questions or find any bug please create [new issue](https://github.com/xlcteam/scoreBoard/issues/new).

## Some screenshots of this application
![dashboard](http://xlcteam.github.com/scoreBoard/imgs/screenshots/0.png)
![group](http://xlcteam.github.com/scoreBoard/imgs/screenshots/5.png)
![match](http://xlcteam.github.com/scoreBoard/imgs/screenshots/7.png)

(c) 2012 - 2014, XLC Team, http://xlc-team.info
