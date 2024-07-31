from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources, principal_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_resources, url_prefix='/principal')

@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response

@app.route('/trigger-fyle-error')
def trigger_fyle_error():
    raise FyleError(status_code=400, message='This is a FyleError')

@app.route('/trigger-validation-error')
def trigger_validation_error():
    raise ValidationError('This is a ValidationError')

@app.route('/trigger-integrity-error')
def trigger_integrity_error():
    raise IntegrityError(statement='dummy statement', params='dummy params', orig='This is an IntegrityError')

@app.route('/trigger-http-exception')
def trigger_http_exception():
    raise HTTPException(description='This is an HTTPException', response=None)

@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err
