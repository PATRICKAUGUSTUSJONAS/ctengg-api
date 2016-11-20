from google.appengine.ext import db
from google.appengine.api import memcache

class User(db.Model):
	username = db.StringProperty(required = True)
	faculty_no = db.StringProperty(required = True)
	email  =db.EmailProperty(required = True)
	api_key = db.StringProperty(required = True)
	admin = db.BooleanProperty()
	banned = db.BooleanProperty()

	@staticmethod
	def get_user(api_key):
		key = 'api'
		user = memcache.get('api')
		if user is None or user.api_key != api_key:
			user = User.all().filter('api_key =', api_key).get()
			memcache.set(key, user)
		return user