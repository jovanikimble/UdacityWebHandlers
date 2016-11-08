# Basic Web Application

import os
import codecs

import webapp2
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):

        items = self.request.get_all("food")
        self.render("shopping_list.html", items = items)

class Rot13Handler(Handler):
    def fill_form(self, t=""):
        self.render("rot13.html",t=t)

    def get(self):
        self.fill_form()
    def post(self):
        user_input = self.request.get('text')
        encrypted_text = encrypt(user_input)
        self.fill_form(encrypted_text)

def encrypt(s):
    lowers = "abcdefghijklmnopqrstuvwxyz"
    uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(0, len(s)):
        char = s[i]
        if char.isalpha():
            if char.islower():
                alpha_pos = lowers.find(char)
                new_char = lowers[(alpha_pos + 13) % 26]
                s = s[:i] + new_char + s[(i + 1):]
            elif char.isupper():
                alpha_pos = uppers.find(char)
                new_char = uppers[(alpha_pos + 13) % 26]
                s = s[:i] + new_char + s[(i + 1):]
    return s

class FizzBuzzHandler(Handler):
    def get(self):
        n = self.request.get('n',0)
        n = n and int(n)
        self.render('fizzbuzz.html', n = n)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/fizzbuzz', FizzBuzzHandler),
                               ('/ROT13', Rot13Handler)
                               ],
                               debug = True)

#"hello, %s" % "steve"
#<ul> = unordered list
# a template library is a library to build complicated strings
#using jinjaz because it is built into google app engine
#os.join is a concatenation. able to do plus as well
#for example:
# >>> import os
# >>> os.path.join("/home", "steve")
# '/home/steve'
# >>>
## Example of %s formatting in python
# >>> "hello, %s" % "steve"
# 'hello, steve'
# **params = extra parameters
#{{variable substitution in jinja2}}
