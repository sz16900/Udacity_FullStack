# Copyright 2016 Google Inc.
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

import webapp2
import cgi

form="""
    <form method="post">
      Whats you bday?
      <br>
      <label>
          Month
          <input type="text" name="month" value="%(month)s">
          </label>
    <label>
        Day
          <input type="text" name="day" value="%(day)s">
          </label>
    <label>
        Year
          <input type="text" name="year" value="%(year)s">
          </label>

      <div style="color:red">%(error)s</div>

      <br>
      <br>
      <input type="submit">

    </form>
"""



class MainPage(webapp2.RequestHandler):

    months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

    month_abbv = dict((m[:3].lower(), m) for m in months)

    def valid_month(self, month):
        if month:
            short_month = month[:3].lower()
            return self.month_abbv.get(short_month)

    def valid_day(self, day):
        if day.isdigit():
            if int(day) > 0 and int(day) <= 31:
                return int(day)

    def valid_year(self, year):
        if year and year.isdigit():
            year = int(year)
            if year >= 1920 and year <= 2020:
                return year

    def escape_html(self, s):
        return cgi.escape(s, quote = True)

    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {'error': error,
                                        'month': self.escape_html(month),
                                        'day': self.escape_html(day),
                                        'year': self.escape_html(year)})

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write(form)
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = self.valid_month(user_month)
        day = self.valid_day(user_day)
        year = self.valid_year(user_year)

        if not (month and day and year):
            # self.response.out.write(form)
            self.write_form("That is not valid", user_month, user_day, user_year)

        else:
            self.redirect("/thanks")
# class TestHandler(webapp2.RequestHandler):
#     def post(self):
#         # q = self.request.get('q')
#         # self.response.out.write(q)
#
#         self.response.headers['Content-Type'] = 'text/plain'
#         # self.response.out.write(self.request)

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks thats a valid day!")


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)
    # ('/testform', TestHandler)
], debug=True)
