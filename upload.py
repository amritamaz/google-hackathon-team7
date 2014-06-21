#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
from google.appengine.api import users
import webapp2
#from PIL import Image

MAIN_PAGE_HTML = """\
<html>
  <body>

    <form action="sign" method="post">
       Title:<textarea name="title" rows="1" cols="60"></textarea>
    <form action="sign" method="post"><br>
       Category:
    <select name="category">
      <option value="project">Project</option>
      <option value="events">Events</option>
    </select> 
    <form action="sign" method="post"><br>
       Description:<textarea name="description" rows="1" cols="60"></textarea>
    <form action="sign" method="post"><br>
       Image:<textarea name="image" rows="1" cols="60"></textarea>
    <form action="sign" method="post"><br>
       Link:<textarea name="link" rows="1" cols="60"></textarea>
      <div><input type="submit" value="Submit"></div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class Guestbook(webapp2.RequestHandler):
    def post(self):
	address = self.request.get('image')
	#self.response.write(address)

        
	self.response.write('<html><body><pre>')
        self.response.write(cgi.escape(self.request.get('title')))
	self.response.write('<br>')
        self.response.write(cgi.escape(self.request.get('category')))
	self.response.write('<br>')
        self.response.write(cgi.escape(self.request.get('description')))
	self.response.write('<br>')       
	#self.response.write(address)
	self.response.write('<img src=%s alt="image" height="42" width="42"> ' % address)	
	#self.response.write('<img src=http://www.clipartbest.com/cliparts/bRi/dn5/bRidn5Bc9.gif alt="image" height="42" width="42"> ')
	self.response.write('<br>')
        self.response.write(cgi.escape(self.request.get('link')))

        self.response.write('</pre></body></html>')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)


