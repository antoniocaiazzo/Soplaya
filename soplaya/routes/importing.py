import uuid

from soplaya.context import app
from flask import make_response, jsonify, url_for

from soplaya.tasks.import_from_csv import ImportFromCSVTask
from soplaya.tasks.manager import TaskManager

manager = TaskManager()

import_data_location = "data/dataset.csv"


@app.route("/import", methods=["GET"])
def importing():
    task_id = str(uuid.uuid4())
    try:
        csv_import = ImportFromCSVTask(task_id, csv_path=import_data_location)
        manager.start_task(csv_import)
    except Exception as e:
        return make_response(jsonify({"message": repr(e)}), 500)
    return make_response(
        jsonify(
            {
                "message": "import job started",
                "resource_id": task_id,
                "status_endpoint": url_for("importing_status", task_id=task_id),
            },
        ),
        201,
    )


@app.route("/import/<task_id>", methods=["GET"])
def importing_status(task_id: str):
    result = manager.get_task_result(task_id)
    if result is None:
        return make_response({"message": "resource not found"}, 404)
    if result.errors:
        return make_response({"message": f"import job {'completed with' if result.done else 'has'} errors", "errors": [repr(e) for e in result.errors]}, 200)
    if not result.done:
        return make_response({"message": "import job in progress"}, 201)
    return make_response({"message": "import job completed successfully"}, 200)
