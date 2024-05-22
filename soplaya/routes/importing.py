from soplaya.context import app
from flask import make_response, jsonify


@app.route("/import", methods=["GET"])
def importing():
    return make_response(jsonify({"message": "import route!"}), 200)
