from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from core.models.teachers import Teacher
from core.libs.exceptions import FyleError

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400

def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

# Edited 

def test_list_teachers(client, h_principal):
    # Assuming there are teachers in the database
    response = client.get('/principal_teacher/teachers', headers=h_principal)

    assert response.status_code == 200
    data = response.json['data']
    assert isinstance(data, list)
    for teacher in data:
        assert 'id' in teacher
        assert 'user_id' in teacher
        assert 'created_at' in teacher
        assert 'updated_at' in teacher

def test_grade_assignment_missing_fields(client, h_principal):
    # Missing 'id' field
    response = client.post('/principal/assignments/grade', json={'grade': 'A'}, headers=h_principal)
    assert response.status_code == 400
    assert response.json['message'] == "Both 'id' and 'grade' are required fields"

    # Missing 'grade' field
    response = client.post('/principal/assignments/grade', json={'id': 1}, headers=h_principal)
    assert response.status_code == 400
    assert response.json['message'] == "Both 'id' and 'grade' are required fields"

def test_grade_assignment_nonexistent_assignment(client, h_principal):
    response = client.post('/principal/assignments/grade', json={'id': -1, 'grade': 'A'}, headers=h_principal)

    assert response.status_code == 404
    assert response.json['message'] == 'No assignment with this id was found'

def test_grade_assignment_draft_assignment(client, h_principal):
    assignment = Assignment.query.get(1)
    assignment.state = AssignmentStateEnum.DRAFT
    response = client.post('/principal/assignments/grade', json={'id': 1, 'grade': 'A'}, headers=h_principal)

    assert response.status_code == 400
    assert response.json['message'] == "Cannot grade an assignment in Draft state"       