from soplaya.context import db


class Report(db.Model):
    __tablename__ = "report"

    date = db.Column(db.Date, nullable=False, primary_key=True)
    restaurant = db.Column(db.String(80), nullable=False, primary_key=True)
    planned_hours = db.Column(db.Integer, nullable=False)
    actual_hours = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Numeric, nullable=False)
    sells = db.Column(db.Numeric, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            "restaurant",
            "planned_hours",
        ),
    )
