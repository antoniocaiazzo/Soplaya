from typing import Type

from flask import request, abort
from flask_sqlalchemy.model import Model
from sqlalchemy import ColumnElement


def get_str_query_param(key: str, default: str = "") -> str:
    return request.args.get(key, default, type=str).lower().strip()


def get_int_query_param(key: str, default: int = None) -> int:
    return request.args.get(key, default, type=int)


def get_all_query_params(exclude: list[str] = None) -> dict[str, any]:
    if exclude is None:
        exclude = []
    return {k: v for k, v in request.args.items() if k not in exclude}


def get_model_field(model: Type[Model], name: str) -> ColumnElement:
    field = getattr(model, name, None)
    if field is None:
        abort(400, f'unknown field "{field}"')
    return field
