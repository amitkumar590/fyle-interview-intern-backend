from flask import Blueprint, request
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher
from core.apis.responses import APIResponse
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.apis.teachers.schema import TeacherSchema
from core import db
from core.apis import decorators
from core.models.assignments import AssignmentStateEnum, GradeEnum

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(principal):
    """View all assignments submitted and/or graded by teachers"""
    assignments = Assignment.query.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    assignments_dump = AssignmentSchema(many=True).dump(assignments)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
def grade_assignment(principal):
    payload = request.json
    assignment_id = payload.get('id')
    grade = payload.get('grade')

    if not assignment_id or not grade:
        return APIResponse.respond_error(message="Both 'id' and 'grade' are required fields", status_code=400)

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return APIResponse.respond_error(message='No assignment with this id was found', status_code=404)

    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.respond_error(message="Cannot grade an assignment in Draft state", status_code=400)

    assignment.grade = grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)
