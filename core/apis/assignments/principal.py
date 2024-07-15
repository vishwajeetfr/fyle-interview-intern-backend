from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of submitted and graded assignments"""
    principal_assignments = Assignment.get_graded_and_submitted_assignments()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)
@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    principal_teachers = Teacher.get_teachers()
    principal_teachers_dump = AssignmentSchema().dump(principal_teachers, many=True)
    return APIResponse.respond(data=principal_teachers_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    graded_assignment = Assignment.principal_mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
    
 