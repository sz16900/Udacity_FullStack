# TO DO:
	#  Get the css file working from the path
	#  Have the name of the logged in person on every page
	#  Style more to make it look better
	#  Ajax
	#  Deploy 



import os
import jinja2
import webapp2
import hashlib
import hmac
import myrot as rot
# import myvalidation as mv
import re
import random
from string import letters

from google.appengine.ext import db

# THIS SHOULD BE BE IN ANOTHER MODULE
secret = "imsoscret"



# Look for these templates in this directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
	autoescape = True)

# HASHING STUFF AND SECURITY


# def hash_str(s):
# 	# return hashlib.md5(s).hexdigest()
# 	return hmac.new(SECRET, s).hexdigest()

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

# APP STUFF

def render_str(template, **kw):
	t = jinja_env.get_template(template)
	return t.render(kw)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	# def render(self, template, **kw):
	# 	self.write(render_str(template, **kw))

	def render_str(self, template, **params):
		params['user'] = self.user
		return render_str(template, **params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def set_secure_cookie(self, name, val):
		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
		    'Set-Cookie',
		    '%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

class MainPage(Handler):
	def get(self):
		# self.response.headers['Content-Type'] = 'text/plain'
		visits = 0
		visit_cookie_str = self.request.cookies.get('visits')
		# Trying to set name welcome page
		# user_cookie_str = self.request.cookie.get()
		if visit_cookie_str:
			cookie_val = check_secure_val(visit_cookie_str)
			if cookie_val:
				visits = int(cookie_val)

		visits += 1

		new_cookie_val = make_secure_val(str(visits))

		self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
		self.write("You visited: %s times" % visits)


		self.render('main.html')

# USER STUFF
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class Rot_13(Handler):
	def get(self):
		self.render('text_area.html')

	def post(self):
		decoder = rot.Myrot()
		text = self.request.get('text')
		text = decoder.rotters(text)
		self.render('text_area.html', text=text)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(Handler):
    def get(self):
        self.render("form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Unit2Signup(Signup):
    def done(self):
        self.redirect('/welcome?username=' + self.username)

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')

class Login(Handler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')

class Unit3Welcome(Handler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')

class Welcome(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')


class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class ASCII(Handler):

	def render_ascii(self, title="", art="", error=""):
		arts = db.GqlQuery('SELECT * FROM Art ORDER BY created DESC')
		self.render('ascii.html', title=title, art=art, error=error, arts=arts)

	def get(self):
		self.render_ascii()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")
		if title and art:
			a = Art(title=title, art=art)
			a.put()

			self.redirect('ascii')
		else:
			error = "We need title and some art!"
			self.render_ascii(title, art, error)

def blog_key(name = 'default'):
	return db.Key.from_path('blogs', name)

class Entry(db.Model):
	title = db.StringProperty(required = True)
	entry = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):

	def render_blog(self, title="", entry="", error=""):
		posts = Entry.all().order('-created')
		# posts = db.GqlQuery('SELECT * FROM Entry ORDER BY created DESC LIMIT 10')
		self.render('blog_posts.html', posts=posts)

	def get(self):
		self.render_blog()

class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Entry', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class BlogEntryForm(Handler):

	def get(self):
		self.render('blog_entry.html')

	def post(self):
		title = self.request.get("title")
		entry = self.request.get("entry")
		if title and entry:
			a = Entry(parent = blog_key(), title=title, entry=entry)
			a.put()

			self.redirect('/blog/%s' % str(a.key().id()))
		else:
			error = "Title and Entry are required!"
			self.render('blog_entry.html' ,title=title, entry=entry, error=error)

app = webapp2.WSGIApplication([
	('/', MainPage),
    ('/rot13', Rot_13),
    ('/signup', Register),
    ('/welcome', Welcome),
	('/ascii', ASCII),
	('/blog', Blog),
	('/blog/entry', BlogEntryForm),
	('/blog/([0-9]+)', PostPage),
	('/unit3/welcome', Unit3Welcome),
   ('/login', Login),
   ('/logout', Logout),
	# ('')
], debug=True)
