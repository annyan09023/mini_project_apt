import webapp2
from google.appengine.api import mail
TEMPLATE = """\
<html>
<head>
<title>Leave a message</title>
<meta charset="utf-8"/>
</head>
<body>
    <form method="post">
        <input name="mail" placeholder="Enter your email">
        <br/>
        <input name="subject" placeholder="Subject">
        <br/>
        <input name="name" placeholder="Enter your name">
        <br/>
        <textarea name="message" style="height:200px;
        weight=500px;"placeholder="Enter your message">
        </textarea>
        <br/>
        <input type="submit" value="Send"/>
        </body>
        </html>
"""
class contact(webapp2.RequestHandler):
  def get(self):
    self.response.write(TEMPLATE)
  def post(self):
# takes input from user
    userMail=self.request.get("mail")
    subject=self.request.get("subject")
    name=self.request.get("name")
    userMessage=self.request.get("message")
   # message=mail.EmailMessage(sender="ann.yanxuebin@gmail.com",subject="Test")

# not tested
    if not mail.is_email_valid(userMail):
      self.response.out.write("Wrong email! Check again!")

   # message.to=userMail
   # print userMail
   # message.body="""Thank you!
   #    You have entered following information:
   #      Your mail: %s
   #        Subject: %s
   #          Name: %s
   #            Message: %s""" %(userMail,subject,name,userMessage)
   # message.send()
    mail.send_mail("ann.yanxuebin@gmail.com", userMail, subject, userMessage)
    self.response.out.write("Message sent!")

app = webapp2.WSGIApplication([('/',contact)], debug=True)
