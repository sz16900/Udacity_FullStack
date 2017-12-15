import os
import jinja2
import webapp2
import myrot as rot
import myvalidation as mv

from google.appengine.ext import db


# Look for these templates in this directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
	autoescape = True)


def render_str(template, **kw):
	t = jinja_env.get_template(template)
	return t.render(kw)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render(self, template, **kw):
		self.write(render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.render('main.html')

class Rot_13(Handler):
	def get(self):
		self.render('text_area.html')

	def post(self):
		decoder = rot.Myrot()
		text = self.request.get('text')
		text = decoder.rotters(text)
		self.render('text_area.html', text=text)

class SignUp(Handler):

	def get(self):
		self.render('form.html')

	def post(self):
		have_error = False
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		check = mv.validation(username, password, email)

		params = dict(username = username, email = email)

		if not check.valid_username():
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not check.valid_password():
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not check.valid_email():
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render('form.html', **params)
		else:
			self.redirect('/welcome?username=' + username)

class Welcome(Handler):
	def get(self):
		username = self.request.get('username')
		self.render('welcome.html', username=username)


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
    ('/signup', SignUp),
    ('/welcome', Welcome),
	('/ascii', ASCII),
	('/blog', Blog),
	('/blog/entry', BlogEntryForm),
	('/blog/([0-9]+)', PostPage),
	# ('')
], debug=True)
