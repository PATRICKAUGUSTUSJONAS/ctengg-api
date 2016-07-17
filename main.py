import webapp2
from handlers.MainPage import MainPage
from handlers.Result import Result
from handlers.Attendance import Attendance


app = webapp2.WSGIApplication([ webapp2.Route(r'/', handler=MainPage, name='home'),
								webapp2.Route(r'/result/', handler = Result, name = 'result'),
								webapp2.Route(r'/attendance/<fac_no>', handler=Attendance, name='attendance')])