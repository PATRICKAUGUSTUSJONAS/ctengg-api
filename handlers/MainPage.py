from handler import *
import webapp2

class MainPage(Handler):
	def get(self):
		self.render("MainPage.html")