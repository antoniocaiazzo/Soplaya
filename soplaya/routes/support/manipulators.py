from typing import Callable, Type, Iterable

from flask import request, make_response, jsonify, url_for, abort, Response
from flask_sqlalchemy.model import Model
from sqlalchemy import asc, desc, Select

from soplaya.context import app, db

pagination_max_per_page = app.config["PAGINATION_MAX_PER_PAGE"]


def get_all_query_params(exclude: list[str] = None) -> dict[str, any]:
    if exclude is None:
        exclude = []
    return {k: v for k, v in request.args.items() if k not in exclude}


def paginate(select: Select, serializer: Callable[[Iterable[Model]], dict[str, any]], endpoint: str) -> Response:
    page = request.args.get("page", None, type=int)
    per_page = request.args.get("size", None, type=int)

    pagination = db.paginate(select, page=page, per_page=per_page, max_per_page=pagination_max_per_page)

    path_params = request.view_args
    query_params = get_all_query_params(exclude=["page"])
    return make_response(
        jsonify(
            {
                "content": serializer(pagination),
                "page": pagination.page,
                "pages": pagination.pages,
                "count": pagination.total,
                **({"next": url_for(endpoint, **path_params, **query_params, page=pagination.next_num)} if pagination.has_next else {}),
                **({"prev": url_for(endpoint, **path_params, **query_params, page=pagination.prev_num)} if pagination.has_prev else {}),
            },
        ),
        200,
    )


def sort_by(model: Type[Model], select: Select) -> Select:
    order_by = request.args.get("order_by", "", type=str).lower().strip()
    order_direction = request.args.get("order", "asc", type=str).lower().strip()

    if not order_by:
        return select
    if order_direction not in ["asc", "desc"]:
        abort(400, 'order must be either "asc" or "desc"')
    field = getattr(model, order_by, None)
    if field is None:
        abort(400, f'unknown field "{field}"')

    order = asc if order_direction == "asc" else desc
    return select.order_by(order(field))
