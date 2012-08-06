from django.contrib.auth.models import User
from django.db import models

from django.contrib import admin
 
class FacebookUser(models.Model):
	facebook_id = models.CharField(max_length=100, unique=True)
	
	# Keep track of the facebook user -> django user mapping
	contrib_user = models.OneToOneField(User)
	contrib_password = models.CharField(max_length=100)

	def __unicode__(self):
		return "%s %s" % (self.contrib_user.first_name, self.contrib_user.last_name)

class FacebookUserAdmin(admin.ModelAdmin):
	pass

admin.site.register(FacebookUser, FacebookUserAdmin)

