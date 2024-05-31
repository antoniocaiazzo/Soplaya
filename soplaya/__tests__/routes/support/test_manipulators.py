import pytest


@pytest.mark.parametrize(
    "page,size,expected",
    (
        (None, None, {"count": 9, "page": 1, "pages": 1}),
        (None, 3, {"count": 9, "next": "/up?size=3&page=2", "page": 1, "pages": 3}),
        (2, 3, {"count": 9, "next": "/up?size=3&page=3", "page": 2, "pages": 3, "prev": "/up?size=3&page=1"}),
        (3, 3, {"count": 9, "page": 3, "pages": 3, "prev": "/up?size=3&page=2"}),
    ),
    ids=["All defaults", "3 pages", "3 pages 2nd page", "3 pages last page"],
)
def test_paginate(app, db, reports_test_data, page, size, expected):
    with app.test_request_context(query_string={"page": page, "size": size}):
        from soplaya.models.Report import Report, ReportSchema
        from soplaya.routes.support.manipulators import paginate

        with app.app_context():
            select = db.select(Report)
            result = paginate(select, lambda r: ReportSchema(many=True).dump(r), "health_route")

        result = {**result.json}
        assert len(result["content"]) == size or result["count"]
        del result["content"]
        assert result == expected


@pytest.mark.parametrize(
    "order_by,order_by_default,order,exception",
    (
        ("date", "", None, False),
        ("date", "", "desc", False),
        (None, "restaurant", "desc", False),
        (None, "", None, False),
        ("date", "", "random", True),
    ),
    ids=["Sort by date default", "Sort by date desc", "Sort by default desc", "Missing order by", "Unknown order direction"],
)
def test_sort_by(app, db, order_by, order_by_default, order, exception):
    with app.test_request_context(query_string={"order_by": order_by, "order": order}):
        from soplaya.models.Report import Report
        from soplaya.routes.support.manipulators import sort_by

        def get_sort_by():
            select = db.select(Report)
            return sort_by(Report, select, default=order_by_default)

        if exception:
            with pytest.raises(Exception):
                get_sort_by()
        elif not order_by and not order_by_default:
            assert "ORDER BY" not in str(get_sort_by())
        else:
            result = get_sort_by()
            assert f"ORDER BY reports.{order_by or order_by_default} {(order or 'asc').upper()}" in str(result)


@pytest.mark.parametrize(
    "lte,gte,expected",
    (
        (None, None, None),
        ("date_lte", None, "WHERE reports.date <= :date_1"),
        (None, "date_gte", "WHERE reports.date >= :date_1"),
        ("date_lte", "date_gte", "WHERE reports.date <= :date_1 AND reports.date >= :date_2"),
    ),
    ids=["No range specified", "Only lte", "Only gte", "Both"],
)
def test_within_range(app, db, lte, gte, expected):
    with app.test_request_context(query_string={lte: "value_lte", gte: "value_gte"}):
        from soplaya.models.Report import Report
        from soplaya.routes.support.manipulators import within_range

        select = db.select(Report)
        result = within_range(Report, select)

        if expected is None:
            assert result == select
        else:
            assert expected in str(result)
