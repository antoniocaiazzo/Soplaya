from typing import Iterable

from soplaya.context import app, db
from soplaya.models.Report import Report, ReportSchema
from soplaya.routes.support.manipulators import paginate, sort_by


def reports_serializer(r: Iterable[Report]) -> dict[str, any]:
    return ReportSchema(many=True).dump(r)


@app.route("/reports", methods=["GET"])
def reports():
    query = sort_by(Report, db.select(Report))
    return paginate(query, reports_serializer, "reports")


@app.route("/reports/restaurant/<name>", methods=["GET"])
def reports_restaurants(name: str):
    query = sort_by(Report, db.select(Report).filter(Report.restaurant == name))
    return paginate(query, reports_serializer, "reports_restaurants")


@app.route("/reports/date/<date>", methods=["GET"])
def reports_dates(date: str):
    query = sort_by(Report, db.select(Report).filter(Report.date == date))
    return paginate(query, reports_serializer, "reports_dates")
