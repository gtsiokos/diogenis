# Diogenis: the online labs registration platform for Technological Institute of Larissa, Greece

Diogenis project is a django-based web application.
It started out as university thesis for students [George Tsiokos](http://georgetsiokos.com/) and [Stefanos Chrousis](https://twitter.com/#!/Lopofsky).
The goal is to solve, with a pragmatic approach, the management of lab registration procedure, since there is no automated system for doing this.

## Setting Up
Get the current dev database and the rest of configurations files, including python modules from [here](http://dl.dropbox.com/u/60164/Web%20Dev/diogenis/DiogenisStarterKit.zip).

* Both <code>diogenis.db</code> and <code>local_settings.py</code> should be placed in the project root directory
* <code>python manage.py syncdb</code>
* <code>python manage.py migrate</code>
* Install the required python modules

Admin Username/Password: <code>admin</code>/<code>1</code>

Users Password: <code>1</code>

Now you have a working draft of Diogenis. :)
#### Remember, with great power. comes great responsibility...

## South
Diogenis uses [South](http://south.aeracode.org/) for database migration. Please read documentation.

### Installing South
<code>sudo easy_install south</code>

### Pulling from Github
* <code>python manage.py syncdb</code>
* <code>python manage.py migrate</code>

### Changes in Models
If you've changed models and before you commit, you do:

* <code>python manage.py syncdb</code>
* <code>python manage.py schemamigration app_name_for_model_you_have_changed --auto</code>

### Starting a New Application
* <code>python manage.py convert_to_south app_name</code>
* <code>python manage.py schemamigration app_name --initial</code>
* <code>python manage.py migrate</code>
