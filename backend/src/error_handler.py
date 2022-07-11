from flask import jsonify


class ApiError(Exception):
    error = 400

    def __init__(self, message, error=None):
        Exception.__init__(self)
        self.message = message
        if error is not None:
            self.error = error

    def to_json(self):
        return jsonify({
            "success": False,
            "error": self.error,
            "message": self.message})
