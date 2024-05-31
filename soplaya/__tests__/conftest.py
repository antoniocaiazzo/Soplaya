import csv
from os import environ
from pathlib import Path

import pytest


@pytest.fixture()
def app():
    environ["DB_URL"] = "sqlite://"
    from soplaya.context import app as _app

    _app.config.update({"TESTING": True, "SQLALCHEMY_TRACK_MODIFICATIONS": False})

    # noinspection PyUnresolvedReferences
    from soplaya.routes.health_check import health_route

    yield _app


@pytest.fixture()
def db(app):
    from soplaya.context import db as _db

    # noinspection PyUnresolvedReferences
    from soplaya.models.Report import Report

    with app.app_context():
        _db.create_all()

    yield _db

    with app.app_context():
        _db.drop_all()


@pytest.fixture()
def test_root_path() -> Path:
    return Path(__file__).resolve().parent


@pytest.fixture()
def test_dataset_path(test_root_path: Path) -> str:
    return f"{test_root_path}/data/test_dataset.csv"


@pytest.fixture()
def reports_test_data(app, db, test_dataset_path: str):
    from soplaya.models.Report import Report

    with open(test_dataset_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        with app.app_context():
            for row in reader:
                report = Report(**row)
                db.session.add(report)
            db.session.commit()
