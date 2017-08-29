import mimetypes

from flask import Flask, url_for
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_jsglue import JSGlue

mimetypes.init()

app = Flask(__name__)
app.config.from_object('config')

app.static_url_path = app.config.get('STATIC_FOLDER')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager(app)

jsglue = JSGlue(app)

from links import helpers, views, models, forms

with app.test_request_context():
    lm.login_view = url_for('login')

# fixme: It's impossible to catch HTTPException. Flask Bug #941 (https://github.com/pallets/flask/issues/941)
from werkzeug.exceptions import default_exceptions
for code, ex in default_exceptions.items():
    app.errorhandler(code)(views.any_error)
