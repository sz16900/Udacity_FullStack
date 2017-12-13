import os 
import jinja2
import webapp2
# import cgi


# Look for these templates in this directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
	autoescape = True)


def rotters(message):
	the_message = ""
	for ch in message:
		# ASCII lower 97-122 (a-z)
		char_ascii = ord(ch)
		if char_ascii >= 97 and char_ascii <=122:

			if (char_ascii + 13) >= 110 and (char_ascii + 13) <= 122:
				the_message = the_message + chr(char_ascii + 13)
			elif (char_ascii - 13) <= 109 and (char_ascii + 13) >= 97:
				the_message = the_message +  chr(char_ascii - 13)

		# ASCII lower 65-90 (A-Z)
		elif char_ascii >= 65 and char_ascii <= 90:
			if (char_ascii + 13) >= 78 and (char_ascii + 13) <= 90:
				the_message = the_message +  chr(char_ascii + 13)
			elif (char_ascii - 13) <= 77 and (char_ascii + 13) >= 65:
				the_message = the_message +  chr(char_ascii - 13)
		else:
			the_message = the_message +  chr(char_ascii)

	return the_message


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **kw):
		t = jinja_env.get_template(template)
		return t.render(kw)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):

		# text = self.request.get('text')
		self.render('text_area.html')

	def post(self):
		text = self.request.get('text')
		text = rotters(text)
		self.render('text_area.html', text = text)

	# def escape_html(self, s):
	# 	return cgi.escape(s, quote = True)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

