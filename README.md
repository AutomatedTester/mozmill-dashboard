Mozmill Dashboard
=======

The starts of a new Mozmill Dashboard with Elastic Search

Installation
=======
* Install elasticsearch
 * Get some elastic search http://www.elasticsearch.org/download/ (i've been using 0.16.5)
 * In the base dir of elastic search uncomment the line that says `discovery.zen.ping.multicast.enabled: false`
 * Run `./bin/elasticsearch` -f to get elastic search running
* Install mysql-server
 * Create a database called "dashboard" using "CREATE DATABASE dashboard;"
* configure settings_local.py to include db configurations
* pip install -r requirements/compiled.txt
* Run `./manage.py syncdb --noinput`
* Run `./manage.py runserver 0.0.0.0:8000`
* Open your browser to `localhost:8000`
