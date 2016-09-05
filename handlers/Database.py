import handler
from python.database import Database
from google.appengine.ext import db

class Register(handler.Handler):
	def get(self):
		self.write("Welcome to the Register page")
		data = db.GqlQuery("SELECT * FROM Database")

		if not data.get():
			a =Database(key_name="14peb049", username = "ArDpPrMaster", faculty = "14PEB049", email = "areeb.jamal@gmail.com", key_api = "DivyaPrakash",admin = 1, banned = 0)
			a.put()
			self.write("generated")