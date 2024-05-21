from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db = SQLAlchemy(app)
