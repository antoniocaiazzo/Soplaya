from marshmallow import Schema, fields as f, validate as v
from sqlalchemy import Computed

from soplaya.context import db


class Report(db.Model):
    __tablename__ = "reports"

    date = db.Column(db.Date, nullable=False, primary_key=True)
    restaurant = db.Column(db.String(80), nullable=False, primary_key=True)
    planned_hours = db.Column(db.Integer, nullable=False)
    actual_hours = db.Column(db.Integer, nullable=False)
    delta_hours = db.Column(db.Integer, Computed(planned_hours - actual_hours))
    budget = db.Column(db.Numeric, nullable=False)
    sells = db.Column(db.Numeric, nullable=False)
    delta_budget = db.Column(db.Numeric, Computed(budget - sells))

    __table_args__ = (
        db.PrimaryKeyConstraint(
            "date",
            "restaurant",
        ),
    )


class ReportSchema(Schema):
    date = f.Date(required=True)
    restaurant = f.String(required=True)
    planned_hours = f.Integer(required=True, validate=v.Range(min=0))
    actual_hours = f.Integer(required=True, validate=v.Range(min=0))
    delta_hours = f.Integer()
    budget = f.Decimal(required=True, validate=v.Range(min=0))
    sells = f.Decimal(required=True, validate=v.Range(min=0))
    delta_budget = f.Decimal()
