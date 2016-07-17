import webapp2
from handlers.MainPage import MainPage


app = webapp2.WSGIApplication([ webapp2.Route(r'/', handler=MainPage, name='home')])