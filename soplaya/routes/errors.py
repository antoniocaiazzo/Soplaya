from flask import make_response, jsonify

from soplaya.context import app


@app.errorhandler(Exception)
def handle_exception(e):
    return make_response(jsonify({"message": repr(e)}), 500)
