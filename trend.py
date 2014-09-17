import webapp2
from google.appengine.api import mail
from google.appengine.api import users
import datetime
class cron_job(webapp2.RequestHandler):
  def get(self):
    mail.send_mail("ann.yanxuebin@gmail.com","ann.yanxuebin@gmail.com","test","test")
app = webapp2.WSGIApplication([('/',cron_job)], debug=True) 
