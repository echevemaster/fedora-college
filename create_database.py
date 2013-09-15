from core import db
import core.models
db.drop_all()
db.create_all()