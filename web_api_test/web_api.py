import cgi
import urllib
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
import webapp2
import json
CREATE_TEMPLATE = """\
   <html>
      <head>
        <title> Create Stream </title>
      </head>
      <body>
         <form action = "/create_handler" enctype = "multipart/form-data" method = "post">
            <div><label>Name Your Stream</label></div>
            <div><textarea name = "stream_name" rows = "1" cols = "60"></textarea></div>
            <div><label>Tag Your Stream</label></div>
            <div><textarea name = "stream_tag" rows = "5" cols = "60"></textarea></div>
            <div><input type = "submit" values = "Create Submit"></div>
         </form>
      </body>
   </html>
"""


class Imag(ndb.Model):
    item = ndb.BlobProperty()
    comment = ndb.StringProperty()
    imag_id = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)

class Stream(ndb.Model):
    user = ndb.UserProperty()
    name = ndb.StringProperty()
    tag = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)
class Create_UI(webapp2.RequestHandler):
    def get(self):
            self.response.write(CREATE_TEMPLATE)
class Create_Handler(webapp2.RequestHandler):
    def get(self):
        stream_query = Stream.query(Stream.name == 'xisha').fetch()
        self.response.write(stream_query[0].name)
        self.response.write(stream_query[0].tag)
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        data = dict()
        data['name'] = stream_query[0].name
        data['tag'] = stream_query[0].tag
        self.response.write(json.dumps(data))
        
    def post(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        data = json.loads(self.request.body)
        stream_name = data.get('stream_name')
        stream_tag = data.get('stream_tag')
        stream_user = users.get_current_user() 
        stream = Stream(user = stream_user,name = stream_name, tag = stream_tag)
        stream.put()
        self.response.write(json.dumps(data))

application = webapp2.WSGIApplication([
    ('/create', Create_UI),
    ('/create_handler', Create_Handler),
],debug = True)

















