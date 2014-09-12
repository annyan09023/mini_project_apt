import cgi
import urllib
from google.appengine.ext import blobstore
#from google.appengine.ext.webapp import blobstore_handler
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
import webapp2

# Create Stream Template
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

#MANAGE_TEMPLATE = """\
#   <html>
#      <head>
#        <title>Manage</title>
#      </head>
#      <body>
#      <h1> Streams I own</h1>
#      <h2> Name      Last Upate     Number of Pictures </h2>
#      <h3><a href = "%s">%s</a>   %s   %s </h3>
#      </body>
#   </html>
#"""
# The model Stream
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
    #imags = ndb.StructuredProperty(Imag, repeated = True)
    #imags = ndb.BlobProperty()
class Create_UI(webapp2.RequestHandler):
    def get(self):
            self.response.write(CREATE_TEMPLATE)

class Create_Handler(webapp2.RequestHandler):
    def post(self):
        stream_name = self.request.get('stream_name')
        stream_tag = self.request.get('stream_tag')
        stream_user = users.get_current_user() 
        stream = Stream(user = stream_user,name = stream_name, tag = stream_tag)
        stream.put()
        self.redirect('/manage')
class View_Single(webapp2.RequestHandler):
    def get(self):
        self.response.write("""\
           <html>
             <head>
              <title>View_Single</title>
             </head>
        """)
        single_stream = Stream.query(Stream.name == self.request.get('stream_name')).fetch()
        self.response.write('<h1>%s</h1>' %single_stream[0].name)
        imags_query = Imag.query(ancestor = single_stream[0].key).fetch()
        if imags_query:
            self.response.write('<h2>Hello!</h2>')
            for imag in imags_query:
                self.response.write(('<div><img src="/img?img_id=%s"></img>') %imag.key.id())
        self.response.write("""\
            <form action="/add?stream_name=%s" enctype = "multipart/form-data" method="post">
            <div><input type = "file" name = "img"/></div>
            <div><input type = "submit" value = "Add Image"></div>
            </form>""" %single_stream[0].name)
        self.response.write('</html>')
        
class Image_Show(webapp2.RequestHandler):
   def get(self):
       imag_query = Imag.query().fetch()
       for imag in imag_query:
           if(imag.key.id()==long(self.request.get('img_id'))):
              self.response.headers['Content-Type']="image/png"
              self.response.write(imag.item)
              break

class Image_Add(webapp2.RequestHandler):
   def post(self):
      add_item = self.request.get('img')
      stream_query = Stream.query(Stream.name == self.request.get('stream_name')).fetch()
      imag_item = Imag(parent = stream_query[0].key)
      imag_item.item = images.resize(add_item,100,100)
      imag_item.put()
      query_params = {'stream_id':stream_query[0].key.id(),'stream_name': stream_query[0].name}
      self.redirect('/viewsinglestream?'+urllib.urlencode(query_params))
         
       
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
	stream_i_owns = Stream.query(Stream.user == users.get_current_user()).order(-Stream.date)
        streams = stream_i_owns.fetch()

        for stream in streams:
            self.response.write('<a href = "/viewsinglestream?stream_id=%s&stream_name=%s">%s</a>' %(stream.key.id(),stream.name,stream.name))
            self.response.write('<hr>')
        self.response.write('</body></html>')

#class View_Single(webapp2.RequestHandler):
 #   def get()

class Login(webapp2.RequestHandler):
    def get(self):
       # self.response.write('<html><title>Please Login</title></html>')
        log_user = users.get_current_user()
        if log_user:
            self.redirect('/create')
        else:
            self.redirect(users.create_login_url('/'))



application = webapp2.WSGIApplication([
    ('/', Login),
    ('/manage',Manage),
    ('/create', Create_UI),
    ('/create_handler', Create_Handler),
    ('/viewsinglestream',View_Single),
    ('/img', Image_Show),
    ('/add', Image_Add),
],debug = True)

















