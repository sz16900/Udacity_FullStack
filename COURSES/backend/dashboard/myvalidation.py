import re

class validation():

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email

	def valid_username(self):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		return self.username and USER_RE.match(self.username)

	def valid_password(self):
		PASS_RE = re.compile(r"^.{3,20}$")
		return self.password and PASS_RE.match(self.password)

	def valid_email(self):
		EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
		return not self.email or EMAIL_RE.match(self.email)