from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.apis.teachers.schema import TeacherSchema

principal_teacher_resources = Blueprint('principal_teacher_resources', __name__)

@principal_teacher_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(principal):
    """View all teachers"""
    teachers = Teacher.query.all()
    teachers_dump = TeacherSchema(many=True).dump(teachers)        
    return APIResponse.respond(data=teachers_dump)

# This file contains the route /teachers (GET) for listing all teachers in the system.