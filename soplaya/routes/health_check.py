from soplaya.context import app
from flask import jsonify, make_response


@app.route("/up", methods=["GET"])
def health_route():
    return make_response(jsonify({"message": "service is up and running"}), 200)
