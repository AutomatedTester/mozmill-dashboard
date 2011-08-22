Mozmill Dashboard
=======

The starts of a new Mozmill Dashboard with Elastic Search

Installation
=======
* [Install elasticsearch](/highriseo/Mozmill-Dashboard-4.0/wiki/Using-Elasticsearch)
* Put some data in elastic search. For now, cd into elasticsearch/grandreset/ and run ./reset
* Install mysql-server
 * Create a database called "dashboard" using "CREATE DATABASE dashboard;"
* `git clone --recursive git://github.com/highriseo/Mozmill-Dashboard-4.0.git`
* configure settings_local.py to include db configurations
* pip install -r requirements/compiled.txt
* Run `./manage.py syncdb --noinput`
* Run `./manage.py runserver 0.0.0.0:8000`
* Open your browser to `localhost:8000`
