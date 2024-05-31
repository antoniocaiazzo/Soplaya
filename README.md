# RestaurantReports

This is a Flask application running in a Docker container. It uses Postgres as the database, running in a separate container.
The app exposes an API with endpoints to import the reports data and provide a way to retrieve and aggregate it by various fields.

The API output is designed so that you can navigate it by using the URL provided in the response.
For example: after triggering the import, `status_endpoint` will contain the link to request to know whether the process has completed or if there were any errors.

## Usage

Run both containers with a single command:

```bash
docker compose up
```

The app will be available on: `https://localhost:4000`

Here are some example requests:

```text
http://localhost:4000/up
http://localhost:4000/import
http://localhost:4000/import/<uuid>
http://localhost:4000/reports
http://localhost:4000/reports?order_by=budget&order=desc&date_gte=2018-01-01
http://localhost:4000/reports/aggregated?group_by=restaurant&date_lte=2019-05-16
```

## Tests

Running tests is just a matter of invoking:

```bash
pytest
```