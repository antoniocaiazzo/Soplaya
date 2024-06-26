from os import environ


SQLALCHEMY_DATABASE_URI = environ.get("DB_URL")

PAGINATION_MAX_PER_PAGE = 100
PAGINATION_PER_PAGE = 20

IMPORT_DATA_LOCATION = "data/dataset.csv"
IMPORT_DATE_FORMAT = "%Y-%m-%d"
IMPORT_CHUNK_SIZE = 32
