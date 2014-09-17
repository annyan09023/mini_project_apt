import cgi
import urllib
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from web_api import *
import webapp2
import json
import httplib
import urllib
import web_api
import mimetypes
import base64
######## For debug#################
global bug
##################################
# Each Imag has a Stream Parent
#class Imag(ndb.Model):
#    pic = ndb.BlobProperty()
#    comment = ndb.StringProperty()
#    imag_id = ndb.IntegerProperty()
#    date = ndb.DateTimeProperty(auto_now_add = True)

#class Stream(ndb.Model):
#    name = ndb.StringProperty()
#    tag = ndb.StringProperty()
#    date = ndb.DateTimeProperty(auto_now_add = True)
#    coverurl = ndb.StringProperty()

#class Webusers(ndb.Model):#Each Webusers xx.key.id() is the user
#    my_stream = ndb.StringProperty(repeated = True) #The id of the stream I own
#    subscribe_stream = ndb.StringProperty(repeated = True)#The id of the stream I subscribe

class Login(webapp2.RequestHandler):
    def get(self):
        log_user = users.get_current_user()
        if log_user:
            self.redirect('/create')
        else:
            self.redirect(users.create_login_url('/'))

#############Create##############
class Create(webapp2.RequestHandler):
    def get(self):
            self.response.write("""\
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
	       <div><label>Cover Image</label></div>
               <div><textarea name = "cover_url" rows = "5" cols = "60"></textarea></div>
               <div><input type = "submit" values = "Create Submit"></div>
            </form>
        </body>
     </html>
""")

class Create_Handler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('stream_name')
        tag = self.request.get('stream_tag')
        coverurl = self.request.get('cover_url'),
        user_id = users.get_current_user().user_id()
        requests = dict()
        requests['stream_tag'] = str(tag)
        requests['stream_name'] = str(name)
        requests['stream_coverurl'] = str(coverurl)
        requests['user_id'] = str(user_id)
        
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost","8080")
        conn.request("POST", "/api_create_a_stream", json.dumps(requests), headers)
        response = conn.getresponse()
        #global bug
        #bug = json.loads(response.read())['id']
        if response.status == 200:
            self.redirect('/manage')
       
class Manage(webapp2.RequestHandler):
   def get(self):
        self.response.write("""\
               <html>
                 <head>
                  <title>Manage</title>
                 </head>
                 <body>
                 <h1> Streams I own</h1>
                 <h2> Name      Last Upate  </h2>
		 """)
        ## Create the new Webusers model
        ##webuser = Webusers(id = users.get_current_user().nickname()) 
        ##webuser.put()
        requests = {
            'user_id': str(users.get_current_user().user_id())
        }	
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost","8080")
        conn.request("POST", "/api_manage", json.dumps(requests), headers)
        responses = conn.getresponse()
        if responses.status == 200:
            data = json.loads(responses.read())
            my_stream = data['my_stream']
            subscribe_stream = data['subscribe_stream']
            self.response.write('<h3>Stream I own</h3>')
            page_range = 'less'##Default value
            for stream in my_stream:
                stream_entity = ndb.Key(Stream,long(stream)).get()
                self.response.write('<a href = "/viewastream?stream_id=%s&stream_name=%s&page_range=%s">%s</a>' %(stream,stream_entity.name,page_range,stream_entity.name))
                self.response.write('<hr>')
            self.response.write('<h4>Stream I subscribe</h4>')
            for stream in subscribe_stream:
                stream_entity = ndb.Key(Stream,long(stream)).get()
                self.response.write('<a href = "/viewastream?stream_id=%s&stream_name=%s&page_range=%s">%s</a>' %(stream,stream_entity.name,page_range,stream_entity.name))
        #global bug
        #bug = responses.status
        #self.response.write('<h5>%s</h5>' %bug)
        self.response.write('</body></html>')

class View_a_stream(webapp2.RequestHandler):
    def get(self):
        self.response.write("""\
           <html>
             <head>
              <title>View_Single</title>
             </head>
        """)
        stream_name = self.request.get('stream_name')
        stream_id = self.request.get('stream_id')
        page_range = self.request.get('page_range')
        requests = {
            'id': str(stream_id),
            'page_range':str(page_range)
        }
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost","8080")
        conn.request("POST", "/api_view_a_stream", json.dumps(requests), headers)
        responses = conn.getresponse()
        urls = json.loads(responses.read())['url_list']
        for url in urls:
            self.response.write('<div><img src=%s></img>' %url)
        if str(page_range) == 'less':
            button_value = 'more'
        else:
            button_value = 'less'
        self.response.write("""\
            <form action="/add?stream_id=%s" enctype = "multipart/form-data" method="post">
            <div><input type = "file" name = "img"/></div>
            <div><input type = "submit" value = "Add Image"></div>
            </form>
            </hr>
            <a href="/viewastream?stream_id=%s&page_range=%s"><input type ="button" value=%s></a>
            """ %(stream_id,stream_id,button_value,button_value))
        #global bug
        #self.response.write("<h1>%s</h1>" %bug)
        self.response.write('</html>')
        
class Image_Show(webapp2.RequestHandler):
   def get(self):
       image_id = long(self.request.get('id'))
       stream_id = long(self.request.get('stream_id'))
       image = ndb.Key(Stream, stream_id, Imag,image_id).get()
       #imag = imag_key.get()
       #imags = Imag.query().fetch()
       #if imags:
         # for imag in imags:
              #if imag.key.id() == long(self.request.get('id')):
       self.response.headers['Content-Type']="image/png"
       self.response.write(image.pic)
       #self.response.write('<html><h1>%s</h1></html>' %imag.key.id())
       
       #self.response.write('<html><h1>%s</h1></html>' %self.request.get('id'))

class Image_Add(webapp2.RequestHandler):
   def post(self):
       stream_id = self.request.get('stream_id')
       pic = self.request.get('img')
       requests = {
            'file': base64.b64encode(pic),
            'stream_id': stream_id
       }
       headers = {"Content-type": "application/json"}
       conn = httplib.HTTPConnection("localhost","8080")
       conn.request("POST", "/api_image_upload", json.dumps(requests), headers)
       responses = conn.getresponse()
       #global bug
       #bug = responses.status
       query_params = {'stream_id':stream_id, 'page_range':'less'}
       if responses.status == 200:
           self.redirect('/viewastream?'+urllib.urlencode(query_params))
      ################for debug##################33
       else:
           self.redirect('/debug?status=%s' %responses.status)
         
class Debug(webapp2.RequestHandler):
    def get(self):
        bug = self.request.get('status')
        #bug = self.request.get('stream_id')
        self.response.write("<html><h1>%s</h1></html>" %bug)
application = webapp2.WSGIApplication([
    ('/',Login),
    ('/create', Create),
    ('/create_handler', Create_Handler),
    ('/manage', Manage),
    ('/viewastream',View_a_stream),
    ('/img',Image_Show),
    ('/add',Image_Add),
    ('/debug',Debug),

],debug = True)














