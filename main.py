# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from handlers.MainPage import MainPage
from handlers.Result import Result
from handlers.Attendance import Attendance
from handlers.Database import Register


app = webapp2.WSGIApplication([ webapp2.Route(r'/', handler=MainPage, name='home'),
								webapp2.Route(r'/result/', handler = Result, name = 'result'),
								webapp2.Route(r'/attendance/<fac_no>', handler=Attendance, name='attendance'),
								webapp2.Route(r'/register', handler=Register, name='register')])