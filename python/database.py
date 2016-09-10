from google.appengine.ext import db

class User(db.Model):
	username = db.StringProperty(required = True)
	faculty_no = db.StringProperty(required = True)
	email  =db.EmailProperty(required = True)
	api_key = db.StringProperty(required = True)
	admin = db.BooleanProperty()
	banned = db.BooleanProperty()