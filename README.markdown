# Diogenis: the online labs registration platform for Technological Institute of Larissa, Greece

Diogenis project is a Django-based web application.
It started out as university thesis for students [George Tsiokos](http://georgetsiokos.com/) and [Stefanos Chrousis](https://twitter.com/#!/Lopofsky).
The goal is to solve, with a pragmatic approach, the management of lab registration procedure, since there is no automated system for doing this.

## Install
Setting up Diogenis should be no trivial for people who already have read the official [Getting Started Tutorial for Django](https://docs.djangoproject.com/en/1.3/intro/tutorial01/).

* <code>pip install -r requirements.txt</code>
* Get also the latest pyCURL package from the respective linux distro software manager
* <code>local_settings.py</code> should be placed in the project root directory
* <code>python manage.py syncdb</code>

Now you have a working draft of Diogenis. :)
