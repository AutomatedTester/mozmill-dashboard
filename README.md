Mozmill Dashboard
=======

The starts of a new Mozmill Dashboard with Elastic Search

Installation
=======

* Install mysql-server
 * Create a database called "dashboard" using "CREATE DATABASE dashboard;"
* configure settings_local.py to include db configurations
* pip install -r requirements/compiled.txt
* Run `./manage.py syncdb --noinput`
* Run `./manage.py runserver 0.0.0.0:8000`
* Open your browser to `localhost:8000`
