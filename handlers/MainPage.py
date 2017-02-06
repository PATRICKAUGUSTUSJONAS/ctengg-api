from handler import *

class MainPage(Handler):
	def get(self):
		self.render("MainPage.html")