import datetime
import random
import string
from functools import wraps

import humanize
import textwrap
from flask import Markup, escape, request
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from werkzeug.exceptions import Forbidden

from links import lm, app
from links.models import User


SIMPLE_CHARS = string.ascii_letters + string.digits


def get_random_string(length=32):
    return ''.join(random.choice(SIMPLE_CHARS) for _ in range(length))


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def context_processor():
    # return dict(pages=Page.query.order_by(Page.id).all(), beers=Beer.query.order_by(Beer.id).all())
    return {}


@app.template_filter('date')
def filter_date(datetime):
    return None if datetime is None else datetime.strftime('%-d %b %Y')


@app.template_filter('dedent')
def filter_dedent(target):
    return None if target is None else textwrap.dedent(target)


@app.template_filter('nl2br')
def filter_nl2br(text):
    return None if text is None else Markup('<br/>\n'.join(escape(text).splitlines()))


@app.template_filter('timedelta')
def filter_timedelta(datetime):
    return None if datetime is None else humanize.naturaltime(datetime)


@app.template_test('older')
def test_older(t1, t2=None, **kwargs):

    if t2 is None:
        t2 = datetime.datetime.now()
    return t1 < t2 - datetime.timedelta(**kwargs)


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated or not current_user.is_active:
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return app.login_manager.unauthorized()
        elif not current_user.admin:
            raise Forbidden()
        return func(*args, **kwargs)
    return decorated_view
