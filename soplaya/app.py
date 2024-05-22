from soplaya.context import app, db

# noinspection PyUnresolvedReferences
from soplaya.models import *

with app.app_context():
    db.create_all()

# noinspection PyUnresolvedReferences
from soplaya.routes import importing
