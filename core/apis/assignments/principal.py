from flask import Blueprint
from core.apis import decorators
from core.models.assignments import Assignment, Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema
from core.apis.responses import APIResponse
from core import db

# created a blueprint to manage all the resources from principal.py only.
principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route("/assignments", methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal

def list_assignments(p):
    pricipal_assignment = Assignment.get_pricipal_assignments()
    principal_assignments_dump = AssignmentSchema().dump( pricipal_assignment, many=True)
    return APIResponse.respond(data=principal_assignments_dump)


@principal_resources.route("/teachers", methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal

def get_teachers(p):
    teacher = Teacher.list_teacher()
    teachers_dump = TeacherSchema().dump(teacher, many=True)
    return APIResponse.respond(data=teachers_dump)


@principal_resources.route("/assignments/grade", methods=['POST'] , strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal

def grade_assignments(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.regrade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade
    )
    
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
