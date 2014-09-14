import json
import httplib
import urllib

globals = {
            "server": "localhost",
           "port"  : "8080",
            "headers": {"Content-type": "application/json", "Accept": "text/plain"},
            #"headers": {"Content-type": "text/html"},
           }

conn = httplib.HTTPConnection(globals["server"],globals["port"])

def send_request(conn, url, req):
     #print '%s' % json.dumps(req)
     conn.request("POST", url, json.dumps(req), globals["headers"])
     #req2 = urllib.urlencode({'stream_name':req['stream_name']});
     #conn.request(method = "POST", url = url2, body = req2)
     resp = conn.getresponse()
     print "status reason"
     print resp.status, resp.reason
     #print resp.read()
     jsonresp = json.loads(resp.read())
     print jsonresp
    #bucket_name = os.environ.get('BUCKET_NAME',
     #print '  %s' % jsonresp
     #return jsonresp

def place_create_request(conn):
     return res

 # many more functions like the above

if __name__ == '__main__':

  service = 'create_handler'
  serviceUrl = '/' + service
#  import random;
#  tmpRequest = str(random.random()) # send any request for now
  tmpRequest = dict()
  tmpRequest['stream_name'] = 'haha'
  tmpRequest['stream_tag'] = 'lala'
  send_request(conn,serviceUrl,tmpRequest)
