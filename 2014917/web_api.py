import cgi
import urllib
from google.appengine.ext import blobstore
#from google.appengine.ext.webapp import blobstore_handler
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
import webapp2
import json
import base64
# Each Imag has a Stream Parent
class Imag(ndb.Model):
    pic = ndb.BlobProperty()
    comment = ndb.StringProperty()
    imag_id = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)

class Stream(ndb.Model):
    #user = ndb.UserProperty()
    #subscribe_user = ndb.UserProperty()
    name = ndb.StringProperty()
    tag = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)
    coverurl = ndb.StringProperty()

class Webusers(ndb.Model):#Each Webusers xx.key.id() is the user
    my_stream = ndb.StringProperty(repeated = True) #The id of the stream I own
    subscribe_stream = ndb.StringProperty(repeated = True)#The id of the stream I subscribe
    
##Management: take a user id and return two lists of streams
class Manage_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        user_id = requests['user_id']
        user_key = ndb.Key(Webusers,user_id)        
        user = user_key.get()
        responses = dict()
        responses['my_stream'] = user.my_stream#id
        responses['subscribe_stream'] = user.subscribe_stream#id
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

##Create a stream: which takes a stream definition and returens a status code
class Create_a_stream_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        stream_tag = requests['stream_tag']
        stream_name = requests['stream_name']
        stream_coverurl = requests['stream_coverurl']
        user_id = requests['user_id'] 
        stream = Stream(name = stream_name, tag = stream_tag, coverurl = stream_coverurl)
        stream_key = stream.put() ##Return stream_id along with the status code for the manage page and then for view_a_stream which needs a stream_id
        user = ndb.Key(Webusers,user_id).get() 
        if user:
            user.my_stream.append(str(stream_key.id()))
            user.put()
        else:
            user = Webusers(id = user_id)
            user.my_stream.append(str(stream_key.id()))
            user.put()
        responses = dict()
        responses['id'] = stream_key.id()
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

## View a stream: which takes a stream id and a page range and returns a list of URLs to images, and a page range
class View_a_stream_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        stream_id = requests['id']
        page_range = requests['page_range']
        #Search for the images under the stream_id
        image_query = Imag.query(ancestor = ndb.Key(Stream, long(stream_id))).order(-Imag.date).fetch()
        image_urls = list()
        #If the page range is 'less' which means should return <=3 urls
        i = 0
        if page_range == 'less' and image_query:
            for image in image_query:
                query_params = {'id':image.key.id(), 'stream_id':stream_id}
                image_urls.append('/img?' + urllib.urlencode(query_params))
                i = i + 1
                if i == 3:
                    break
        if page_range == 'more' and image_query:
           for image in image_query:
                query_params = {'id':image.key.id(), 'stream_id':stream_id}
                image_urls.append('/img?' + urllib.urlencode(query_params))
        responses = dict()
        responses['url_list'] = image_urls
        responses['page_range'] = page_range
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

## Image Upload: Takes a stream id and a file
#class Image_Upload_api(webapp2.RequestHandler):
#    def post(self):
#        requests = json.loads(self.request.body)
#        stream_id = requests['stream_id']
#        pic = requests['file']
#        image = Imag(parent = ndb.Key(Stream, long(stream_id)))
#        image.pic = images.resize(pic, 300, 300)
#        image.put()

class Image_Upload_api(webapp2.RequestHandler):
    def post(self):
        responses = json.loads(self.request.body)
        pic = base64.b64decode(responses['file'])
        stream_id = responses['stream_id']
        imag = Imag(parent = ndb.Key(Stream, long(stream_id)))
        imag.pic = images.resize(pic,100,100)
        imag.put()

## View all streams: which returns a list of names of streams and their cover images
class View_all_streams_api(webapp2.RequestHandler):
    def post(self):
        streams = Stream.query().fetch()
        responses = dict()
        responses['names'] = list()
        responses['coverurls'] = list()
        for stream in streams:
            responses['names'].append(stream.name)
            responses['coverurls'].append(stream.coverurl)
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

## Search streams: which takes a query string and returns a list of streams(titles and cover image urls) that contain matching text
class Search_streams_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        query_string = requests['query_string']
        streams = Stream.query().fetch()
        responses = dict()
        responses['names'] = list()
        responses['coverurls'] = list()
        for stream in streams:
            if query_string in stream.name:
                responses['names'].append(stream.name)
                responses['coverurls'].append(stream.coverurl)
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

## Most viewed Streams: which returns a list of streams sorted by recent access frequency
class Most_viewed_streams_api(webapp2.RequestHandler):
    def post(self):
        responses = dict()
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))


## Reporting requests:
##class Report_requests(webapp2.RequestHandler):
##    def post(self):

application = webapp2.WSGIApplication([
    ('/api_manage',Manage_api),
    ('/api_create_a_stream', Create_a_stream_api),
    ('/api_view_a_stream', View_a_stream_api),
    ('/api_view_all_streams', View_all_streams_api),
    ('/api_image_upload', Image_Upload_api),
    ('/api_search_streams', Search_streams_api),
    ('/api_most_viewed_streams', Most_viewed_streams_api),
],debug = True)














