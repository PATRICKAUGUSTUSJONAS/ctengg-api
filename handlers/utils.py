import json

from google.appengine.api import memcache
from google.appengine.api import urlfetch

from db.models import CacheData
from db.models import User


def verify_api_key(api_key):
    data = {'error': True, 'message': "URL must contain API Key : 'api_key'"}
    if api_key:
        user = User.get_user(api_key)
        if user and not user.banned:
            data = {'error': False, 'user': user}
        elif user and user.banned:
            data = {'error': True, 'message': 'API key is banned or not activated yet'}
        else:
            data = {'error': True, 'message': 'No such API key in database'}
    return data


def verify_page(doc):
    data = dict()
    data['error'] = False
    if '404' in doc:
        data['error'] = True
        data['message'] = 'Server is down! Please try again'
    elif 'alert' in doc:
        data['error'] = True
        data['message'] = (doc.split("'"))[1].split("'")[0]

    return data


def fetch_item(url, fetch):
    doc = urlfetch.fetch(url)

    data = verify_page(doc.content)
    if data['error']:
        return data

    try:
        data = fetch(doc.content)
        data['error'] = False
        data['message'] = 'Successful'
    except AttributeError:
        data['error'] = True
        data['message'] = 'Parse Error'

    return data


def get_item(key, user, cached, get_method):
    data = memcache.get(key)

    if data is None or data['error'] or not cached:
        store_data = CacheData.get_by_id(key)

        if store_data is None or json.loads(store_data.data)['error'] or not cached:
            data = get_method()
            if not data['error']:
                store_data = CacheData(id=key)
                store_data.request = key
                store_data.data = json.dumps(data)
                store_data.put()
        else:
            data = json.loads(store_data.data)
        data['user'] = user.username
        memcache.set(key, data)

    return data


def get_complete_attendance(user, use_stored=True):
    from CompleteAttendance import CompleteAttendance
    key = 'complete_attendance'
    url = 'http://ctengg.amu.ac.in/web/cattendance.php?p=btech'
    return get_item(key, user, use_stored, lambda: fetch_item(url, CompleteAttendance.parse))


def get_course_attendance(course, user, use_stored=True):
    from CompleteAttendance import ClassAttendance
    key = 'course_' + course
    return get_item(key, user, use_stored, lambda: ClassAttendance.get_attendance_by_fetch(course))


def get_result(fac_no, enrol_no, user, use_stored=True):
    from Result import Result
    key = 'result_' + fac_no.upper() + ':' + enrol_no.upper()
    url = 'http://ctengg.amu.ac.in/web/table_resultnew.php?' + 'fac=' + fac_no + '&en=' + enrol_no + '&prog=btech'
    return get_item(key, user, use_stored, lambda: fetch_item(url, Result.parse_result))


def get_attendance(fac_no, user, use_stored=True):
    from Attendance import Attendance
    key = 'attendance_' + fac_no.upper()
    url = 'http://ctengg.amu.ac.in/web/table.php?id=' + fac_no
    return get_item(key, user, use_stored, lambda: fetch_item(url, Attendance.parse_attendance))

