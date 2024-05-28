from typing import Callable, Type, Iterable

from flask import request, make_response, jsonify, url_for, abort, Response
from flask_sqlalchemy.model import Model
from sqlalchemy import asc, desc, Select

from soplaya.context import app, db
from soplaya.routes.support.utils import get_int_query_param, get_str_query_param, get_all_query_params, get_model_field

pagination_max_per_page = app.config["PAGINATION_MAX_PER_PAGE"]


def paginate(select: Select, serializer: Callable[[Iterable[Model]], list[dict[str, any]]], endpoint: str) -> Response:
    page = get_int_query_param("page")
    per_page = get_int_query_param("size")

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


def sort_by(model: Type[Model], select: Select, default: str = "") -> Select:
    order_by = get_str_query_param("order_by", default)
    order_direction = get_str_query_param("order", "asc")

    if not order_by:
        return select
    if order_direction not in ["asc", "desc"]:
        abort(400, 'order must be either "asc" or "desc"')

    field = get_model_field(model, order_by)
    order = asc if order_direction == "asc" else desc

    return select.order_by(order(field))
