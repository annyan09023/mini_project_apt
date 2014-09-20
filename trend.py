import webapp2
from google.appengine.api import mail
from google.appengine.api import users
import datetime
TEMPLATE = """
<html>
<head>
<title>Trend</title>
</head>
<body>
  <form method = "post">
  Current Rate<br>
  <input type="radio" name ="rate" value="0">No reprots<br>
  <input type="radio" name ="rate" value="1">Every 1 minutes<br>
  <input type="radio" name ="rate" value="2">Every 2 minutes<br>
  <input type="radio" name ="rate" value="4">Every 4 minutes<br>
  <input type="submit" value="Update Rate">
  </form>
</body>
</html>
"""
global count
count = 0
global rate
class cron_job_ui(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(TEMPLATE)
  def post(self):
    global rate
    rate= self.request.get('rate')
    self.redirect('/count')
class count_job(webapp2.RequestHandler):
  def get(self):
    global count
    count = count+1
   # try: 
   #   count = int(float(self.request.get('count')))
   #   count = count+1
    print count
    global rate
    print rate
    if rate !=0:
      if int(count)%int(rate)==0:
        mail.send_mail("ann.yanxuebin@gmail.com","ann.yanxuebin@gmail.com","test","test")
#class sendmail(webapp2.RequestHandler):
#  def get(self):
#    rate = int(float(self.request.get('rate')))
#    count = int(float(self.request.get('count')))
#    print "rate%s"%rate
#    print count
#    if rate !=0:
#      if count%rate==0:
#        mail.send_mail("ann.yanxuebin@gmail.com","ann.yanxuebin@gmail.com","test","test")
#    #if rate!=0:
#    #  if count==rate:
#    #    mail.send_mail("ann.yanxuebin@gmail.com","ann.yanxuebin@gmail.com","test","test")
#    #    count=1
#    #  count = count+1
app = webapp2.WSGIApplication([('/',cron_job_ui),('/count',count_job)], debug=True) 
