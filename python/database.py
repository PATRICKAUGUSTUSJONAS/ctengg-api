from google.appengine.ext import db

class Database(db.Model):
	username = db.StringProperty(required = True)
	faculty = db.StringProperty(required = True)
	email  =db.EmailProperty(required = True)
	key_api = db.StringProperty(required = True)
	admin = db.IntegerProperty()
	banned = db.IntegerProperty()

