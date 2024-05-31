import pytest


def test_get_str_query_param(app):
    with app.test_request_context(query_string={"key": "   TEST "}):
        from soplaya.routes.support.utils import get_str_query_param

        result = get_str_query_param("key")

    assert result == "test"


def test_get_int_query_param(app):
    with app.test_request_context(query_string={"key": "123 "}):
        from soplaya.routes.support.utils import get_int_query_param

        result = get_int_query_param("key")

    assert result == 123


def test_get_all_query_params(app):
    with app.test_request_context(query_string={"key1": "   TEST ", "key2": "123 ", "page": "5"}):
        from soplaya.routes.support.utils import get_all_query_params

        result = get_all_query_params(exclude=["page"])

    assert result == {"key1": "   TEST ", "key2": "123 "}


def test_get_model_field(app):
    from soplaya.models.Report import Report
    from soplaya.routes.support.utils import get_model_field

    result = get_model_field(Report, "restaurant")
    assert result == Report.restaurant


def test_get_model_field_not_found(app):
    from soplaya.models.Report import Report
    from soplaya.routes.support.utils import get_model_field

    with pytest.raises(Exception):
        get_model_field(Report, "name")
