from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.query.filter(
        Assignment.teacher_id == p.teacher_id, 
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    )
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    if not assignment:
        return APIResponse.respond_error_with_details(message='No assignment with this id was found', status_code=404, error='FyleError')

    if assignment.teacher_id != p.teacher_id:
        return APIResponse.respond_error_with_details(message='This assignment belongs to a different teacher', status_code=400, error='FyleError')

    if assignment.state != AssignmentStateEnum.SUBMITTED:
        return APIResponse.respond_error_with_details(message='Only a submitted assignment can be graded', status_code=400, error='FyleError')

    if grade_assignment_payload.grade not in GradeEnum.__members__:
        return APIResponse.respond_error_with_details(message='Invalid grade', status_code=400, error='ValidationError')

    assignment.grade = grade_assignment_payload.grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=graded_assignment_dump)
