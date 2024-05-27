from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("soplaya.config")
app.config.from_envvar("SOPLAYA_CONFIG")
db = SQLAlchemy(app)
