from google.appengine.ext import ndb
from google.appengine.api import memcache


class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    faculty_no = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    api_key = ndb.StringProperty(required=True)
    admin = ndb.BooleanProperty()
    banned = ndb.BooleanProperty()

    @staticmethod
    def get_user(api_key):
        key = 'api'
        user = memcache.get('api')
        if user is None or user.api_key != api_key:
            user = User.query(User.api_key == api_key).get()
            memcache.set(key, user)
        return user


class RequestLog(ndb.Model):
    data = ndb.StringProperty(required=True, indexed=False)
    attendance = ndb.BooleanProperty(required=True, indexed=False)
    requests = ndb.IntegerProperty(required=True, default=0, indexed=False)
    access_time = ndb.DateTimeProperty(auto_now=True, indexed=False)


class CacheData(ndb.Model):
    data = ndb.StringProperty(required=True, indexed=False)
    request = ndb.StringProperty(required=True, indexed=False)
