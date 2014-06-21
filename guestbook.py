import cgi
import urllib
import os

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

JINJA_ENVIRONMENT.filters['datetimeformat'] = datetimeformat


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    title = ndb.StringProperty(indexed=False)
    category = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    image = ndb.StringProperty(indexed=False)
    types = ndb.StringProperty(indexed=False)
    link = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


    projects = ndb.DateTimeProperty(auto_now_add=True)
    outreach = ndb.DateTimeProperty(auto_now_add=True)
    women = ndb.DateTimeProperty(auto_now_add=True)
    elementary = ndb.DateTimeProperty(auto_now_add=True)
    highschool = ndb.DateTimeProperty(auto_now_add=True)
    middleschool = ndb.DateTimeProperty(auto_now_add=True)
    college = ndb.DateTimeProperty(auto_now_add=True)
    veterans = ndb.DateTimeProperty(auto_now_add=True)
    disabilities = ndb.DateTimeProperty(auto_now_add=True)
    minorities = ndb.DateTimeProperty(auto_now_add=True)
    events = ndb.DateTimeProperty(auto_now_add=True)
    hackathons = ndb.DateTimeProperty(auto_now_add=True)
    techtalks = ndb.DateTimeProperty(auto_now_add=True)
    jobfairs = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            login_logout_text = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_logout_text = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'login_logout_text': login_logout_text,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class UploadPage(webapp2.RequestHandler):
    def get(self):
        #self.response.write(MAIN_PAGE_HTML)
        template = JINJA_ENVIRONMENT.get_template('form.html')
        self.response.write(template.render())


class MyBucketsPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-(Greeting.date))
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            login_logout_text = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_logout_text = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'login_logout_text': login_logout_text,
        }

        template = JINJA_ENVIRONMENT.get_template('mybuckets.html')
        self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        address = self.request.get('image')

        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.title = cgi.escape(self.request.get('title'))
        greeting.category = cgi.escape(self.request.get('category'))
        greeting.types = cgi.escape(self.request.get('types'))
        greeting.description = cgi.escape(self.request.get('description'))
        greeting.image = address
        greeting.link = cgi.escape(self.request.get('link'))
  #       greeting.projects = cgi.escape(self.request.get('projects'))
		# greeting.outreach = cgi.escape(self.request.get('outreach'))
		# greeting.women = cgi.escape(self.request.get('women'))
		# greeting.elementary = cgi.escape(self.request.get('elementary'))
		# greeting.highschool = cgi.escape(self.request.get('highschool'))
		# greeting.middleschool = cgi.escape(self.request.get('middleschool'))
		# greeting.college = cgi.escape(self.request.get('college'))
		# greeting.veterans = cgi.escape(self.request.get('verterans'))
		# greeting.disabilities = cgi.escape(self.request.get('disabilities'))
		# greeting.minorities = cgi.escape(self.request.get('minorities'))
		# greeting.events = cgi.escape(self.request.get('events'))
		# greeting.hackathons = cgi.escape(self.request.get('hackathons'))
		# greeting.techtalks = cgi.escape(self.request.get('techtalks'))
		# greeting.jobfairs = cgi.escape(self.request.get('jobfairs'))

        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadPage),
    ('/mybuckets', MyBucketsPage),
    ('/sign', Guestbook),
], debug=True)
