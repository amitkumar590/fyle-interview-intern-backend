from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    if incoming_payload.get('content') is None:
        return APIResponse.respond_error(message='Content cannot be null', status_code=400)

    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(submit_assignment_payload.id)
    if not assignment:
        return APIResponse.respond_error(message='No assignment found with the given ID', status_code=404)

    if assignment.student_id != p.student_id:
        return APIResponse.respond_error(message='This assignment does not belong to the current student', status_code=403)

    if assignment.content is None:
        return APIResponse.respond_error(message='Assignment content cannot be empty', status_code=400)

    if assignment.state != AssignmentStateEnum.DRAFT:
        return APIResponse.respond_error_with_details(message='only a draft assignment can be submitted', status_code=400, error='FyleError')    

    assignment.state = AssignmentStateEnum.SUBMITTED
    assignment.teacher_id = submit_assignment_payload.teacher_id
    db.session.commit()

    submitted_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=submitted_assignment_dump)