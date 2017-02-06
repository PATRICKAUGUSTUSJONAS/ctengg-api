import os

import jinja2
import webapp2

template_dir = os.path.join(os.path.split(os.path.dirname(__file__))[0], "template")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

        # This is the basic handler class that will be inherited to create class like Mainpage
        # This class provide functions such as write render_str and render
        # write - used write the responses on the screen
        # render - used to provide the vlaue of the variable in the templates and then reload the html
        # render_str - used to the mideval function used to render the parameters into the template
