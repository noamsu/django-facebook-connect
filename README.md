About 
==============

This package adds facebook connect authentication to a Django web
site. Many of the existing packages are either out of date, using soon to be deprecated facebook
apis (along with out of date documentation), or simply do not work quite right. 

This package is small, does not have external dependencies, and should "just work".


Install
==============

You will need to create a Facebook application for facebook connect to work.

Set the "Site URL", located in your facebook applications settings to:

	http://<your-project's-address>/facebook_connect

Note: during development, you may set the above to localhost, e.g. http://127.0.0.1:8000/facebook_connect

Next, install this package by running:

	pip install django-facebook-connect

Configure the following settings in your settings.py:

	FACEBOOK_LOGIN_REDIRECT = "/"                              # (optional, defaults to "/")
	
	FACEBOOK_APP_ID = "<place your app id here>"               # required
	
	FACEBOOK_APP_SECRET = "<place your app secret code here>"  # required
	
	FACEBOOK_SCOPE = "email"						           # (optional, defaults to "email")

Note: FACEBOOK_SCOPE determines what permissions facebook will ask from your users,
	  and in turn, give you access to. For example, your scope may look like:
	  'read_stream,publish_stream,offline_access,user_photos', whereas above
	  we are only asking for email access. This package comes with the
	  python_facebook_sdk included for retrieving user information - but
	  does not gather more than the name and email at this time (perhaps
	  in future versions).

Add "facebook_connect" to your list of installed apps:

	INSTALLED_APPS = (
    	'facebook_connect',
	)

And include faceboook_connect.urls within your urls.py:

	urlpatterns = pattern('',
  
   		(r'^facebook_connect/', include('facebook_connect.urls')),

	)

Finally, run:

	python manage.py syncdb 

Or, if you're using South:

	python manage.py schemamigration facebook_connect --initial

to create the initial migration, and

	python manage.py migrate facebook_connect

to migrate the database.

Usage
==============

These tags are now usable in your templates:

	{% load facebook_connect %}
	
	{% facebook_button %}                

	{% facebook_script %}


If you would like to override the default button (facebook_button tag), to choose a different image and have more control, you'll need to trigger (on click) the 'facebook_connect()' function that starts the login process.

Credits
==============

Inspiration was taken from this "django-facebookconnect" package: https://github.com/teebes/django-facebookconnect/
as well as the views/models responsible for the facebook --> django user mapping.

Security code for validating the signedRequest is by Sunil Arora:
http://sunilarora.org/parsing-signedrequest-parameter-in-python-bas
