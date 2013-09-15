import flask
from core import db
import core.models
app = flask.Flask(__name__)
db.init_app(app)
with app.test_request_context():
   db.drop_all()
   db.create_all()