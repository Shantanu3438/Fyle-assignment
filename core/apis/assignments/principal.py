from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher

from .schema import AssignmentSchema, TeacherSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    assignments = Assignment.get_submitted_and_graded_assignments()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_all_teachers(p):
    all_teachers = Teacher.get_all_teachers()
    all_teachers_dump = TeacherSchema().dump(all_teachers, many=True)
    return APIResponse.respond(data=all_teachers_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_students(p, incoming_payload):
    grade_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.get_by_id(grade_payload.id)
    if assignment.state == AssignmentStateEnum.DRAFT:
        return (APIResponse.respond(data="A Draft Assignment cannot be graded."), 400)
    assignment = Assignment.mark_grade(grade_payload.id, grade_payload.grade, auth_principal=p)
    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(assignment_dump)
