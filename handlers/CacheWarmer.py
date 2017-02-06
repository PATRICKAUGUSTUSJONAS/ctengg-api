import time

import webapp2

from utils import *


class CacheWarmer(webapp2.RequestHandler):
    @staticmethod
    def substring(full, sub):
        return full[full.index(sub) + len(sub):]

    @staticmethod
    def warm_cache(user, cache_enabled=False):
        data = dict()
        data['attendance'] = 0
        data['result'] = 0
        data['course'] = 0
        data['complete'] = 0

        cached = CacheData.query()
        for entry in cached.iter():
            request = entry.request
            if 'attendance_' in request:
                get_attendance(CacheWarmer.substring(request, 'attendance_'), user, cache_enabled)
                data['attendance'] += 1
            elif 'result_' in request:
                fac, en = request.split(':')
                fac = CacheWarmer.substring(fac, 'result_')
                get_result(fac, en, user, cache_enabled)
                data['result'] += 1
            elif 'course_' in request:
                get_course_attendance(CacheWarmer.substring(request, 'course_'), user, cache_enabled)
                data['course'] += 1
            elif 'complete_' in request:
                get_complete_attendance(user, cache_enabled)
                data['complete'] += 1

        return data

    def get(self):
        start = time.time()
        api_key = self.request.get("api_key")

        data = verify_api_key(api_key)
        if not data['error']:
            cached = self.request.get('cached')
            data = CacheWarmer.warm_cache(data.pop('user'), cached)

        data['time'] = time.time() - start
        json_out = json.dumps(data, ensure_ascii=False, indent=2)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json_out)
