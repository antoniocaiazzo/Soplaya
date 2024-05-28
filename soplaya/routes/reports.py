from typing import Iterable

from flask import abort, make_response, jsonify
from sqlalchemy import func

from soplaya.context import app, db
from soplaya.models.Report import Report, ReportSchema
from soplaya.routes.support.manipulators import paginate, sort_by
from soplaya.routes.support.utils import get_str_query_param, get_model_field


def reports_serializer(r: Iterable[Report]) -> list[dict[str, any]]:
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


@app.route("/reports/aggregated", methods=["GET"])
def reports_aggregated():
    group_by = get_str_query_param("group_by")

    if not group_by:
        abort(400, 'missing parameter: "group_by"')
    if group_by not in ["date", "restaurant"]:
        abort(400, f'invalid group_by parameter: "{group_by}"')

    aggregated_field = get_model_field(Report, group_by)
    collapsed_field = Report.date if group_by == "restaurant" else Report.restaurant

    query = sort_by(
        Report,
        db.select(
            aggregated_field,
            func.count(collapsed_field).label(f"{collapsed_field.name}s"),
            func.sum(Report.planned_hours).label("planned_hours"),
            func.sum(Report.actual_hours).label("actual_hours"),
            func.sum(Report.delta_hours).label("delta_hours"),
            func.sum(Report.budget).label("budget"),
            func.sum(Report.sells).label("sells"),
            func.sum(Report.delta_budget).label("delta_budget"),
        ).group_by(aggregated_field),
        default=group_by,
    )

    result = db.session.execute(query).mappings()
    return make_response(jsonify([dict(r) for r in result]), 200)
