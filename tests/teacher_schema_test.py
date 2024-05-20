from marshmallow import ValidationError
import pytest
from core.apis.teachers.schema import TeacherSchema, TeacherCreateSchema, TeacherUpdateSchema

@pytest.fixture
def teacher_data():
    return {
        'id': 1,
        'user_id': 1001,
        'created_at': '2022-01-01T12:00:00',
        'updated_at': '2022-01-02T10:00:00'
    }

def test_teacher_schema_load(teacher_data):
    schema = TeacherSchema()
    loaded_teacher = schema.load(teacher_data)
    assert loaded_teacher.user_id == teacher_data['user_id']

def test_teacher_schema_dump(teacher_data):
    schema = TeacherSchema()
    teacher = schema.load(teacher_data)
    dumped_teacher = schema.dump(teacher)
    assert dumped_teacher['user_id'] == teacher_data['user_id']

def test_teacher_create_schema_load():
    schema = TeacherCreateSchema()
    teacher_data = {'user_id': 1001}
    loaded_teacher = schema.load(teacher_data)
    assert loaded_teacher.user_id == teacher_data['user_id']

def test_teacher_create_schema_load_missing_user_id():
    schema = TeacherCreateSchema()
    with pytest.raises(ValidationError):
        schema.load({})

def test_teacher_update_schema_load():
    schema = TeacherUpdateSchema()
    teacher_data = {'user_id': 1001}
    loaded_teacher = schema.load(teacher_data)
    assert loaded_teacher.user_id == teacher_data['user_id']

def test_teacher_update_schema_load_none_user_id():
    schema = TeacherUpdateSchema()
    teacher_data = {'user_id': None}
    loaded_teacher = schema.load(teacher_data)
    assert loaded_teacher.user_id == teacher_data['user_id']
