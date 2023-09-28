from flask import render_template, jsonify

from yacut import app, db


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def _todict(self):
        return dict(message=self.message)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def iternal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error._todict()), error.status_code
