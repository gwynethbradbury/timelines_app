from flask import Markup
from flasktasks import app
from flasktasks.plugins import dispatch


@app.template_filter('html_dispatch')
def html_dispatch(storyline, function):
    values = dispatch(function, storyline)
    return Markup(''.join(values))
