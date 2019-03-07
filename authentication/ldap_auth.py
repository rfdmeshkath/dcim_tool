from functools import wraps
from flask import request, Response, render_template, session

from authentication.ldap_config import allowed_access


def check_auth(username, password):
    return allowed_access(username, password)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(render_template('authentication_required.html'), 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})
        else:
            session['username'] = auth.username
            return f(*args, **kwargs)
    return decorated
