import time
import json
import webapp2
from Attendance import Attendance
from Result import Result
from CompleteAttendance import ClassAttendance
from CompleteAttendance import CompleteAttendance
from db.models import User
from db.models import CacheData

class CacheWarmer(webapp2.RequestHandler):

	@staticmethod
	def substring(full, sub):
		return full[full.index(sub) + len(sub):]

	@staticmethod
	def warm_cache(user, cache_enabled = False):
		data = dict()
		data['attendance'] = 0
		data['result'] = 0
		data['course'] = 0
		data['complete'] = 0
		
		cached = CacheData.query()
		for entry in cached.iter():
			request = entry.request
			if 'attendance_' in request:
				Attendance.get_attendance(CacheWarmer.substring(request, 'attendance_'), user, cache_enabled)
				data['attendance'] += 1
			elif 'result_' in request:
				fac, en = request.split(':')
				fac = CacheWarmer.substring(fac, 'result_')
				Result.get_result(fac, en, user, cache_enabled)
				data['result'] += 1
			elif 'course_' in request:
				ClassAttendance.get_attendance(CacheWarmer.substring(request, 'course_'), user, cache_enabled)
				data['course'] += 1
			elif 'complete_' in request:
				CompleteAttendance.get_attendance(user, cache_enabled)
				data['complete'] += 1

		return data

	def get(self):
		start = time.time()
		api_key = self.request.get("api_key")
		if api_key:
			user = User.get_user(api_key)
			if user and not user.banned :
				cached = False
				if self.request.get('cached'):
					cached = True
				data = CacheWarmer.warm_cache(user, cached)
			elif user and user.banned :
				data = {'error':True, 'message':'API key is banned or not activated yet'}
			else :
				data = {'error':True, 'message':'No such API key in database'}

		data['time'] = time.time() - start
		json_out = json.dumps(data, ensure_ascii=False, indent=2)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json_out)
