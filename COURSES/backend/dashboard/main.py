import os 
import jinja2
import webapp2
import myrot as rot
import myvalidation as mv


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


app = webapp2.WSGIApplication([
	('/', MainPage),
    ('/rot13', Rot_13),
    ('/signup', SignUp),
    ('/welcome', Welcome)
], debug=True)

