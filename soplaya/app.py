from soplaya.context import app, db

# noinspection PyUnresolvedReferences
from soplaya.models.Report import Report

with app.app_context():
    db.create_all()

# noinspection PyUnresolvedReferences
from soplaya.routes.health_check import *

# noinspection PyUnresolvedReferences
from soplaya.routes.errors import *

# noinspection PyUnresolvedReferences
from soplaya.routes.importing import *

# noinspection PyUnresolvedReferences
from soplaya.routes.reports import *
