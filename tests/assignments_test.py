import pytest
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from unittest.mock import patch, Mock
from core.apis.decorators import AuthPrincipal

def test_repr_assignment():
    assignment = Assignment(id=1)
    assert repr(assignment) == '<Assignment 1>'

@pytest.fixture
def mock_assignment():
    return Mock(spec=Assignment, id=1, state=AssignmentStateEnum.DRAFT)

def test_upsert_existing_assignment(mock_assignment):
    with patch('core.models.assignments.Assignment.get_by_id', return_value=mock_assignment), \
         patch('core.models.assignments.db.session.flush') as mock_flush:
        
        updated_content = "Updated content"
        mock_assignment_new = Mock(spec=Assignment, id=1, content=updated_content)

        # Call the upsert method
        updated_assignment = Assignment.upsert(mock_assignment_new)

        # Assertions
        assert updated_assignment == mock_assignment  # Ensure the returned assignment is the same as the mock
        assert mock_assignment.content == updated_content  # Ensure the content is updated
        mock_flush.assert_called_once()  # Ensure session flush is called

def test_upsert_new_assignment():
    with patch('core.models.assignments.db.session.add') as mock_add, \
         patch('core.models.assignments.db.session.flush') as mock_flush:
        
        new_content = "New assignment content"
        mock_assignment_new = Mock(spec=Assignment, id=None, content=new_content)

        # Call the upsert method
        new_assignment = Assignment.upsert(mock_assignment_new)

        # Assertions
        assert new_assignment == mock_assignment_new  # Ensure the returned assignment is the same as the mock
        mock_add.assert_called_once_with(mock_assignment_new)  # Ensure session add is called with the new assignment
        mock_flush.assert_called_once()  # Ensure session flush is called

def test_submit_assignment(client, h_student_1):
    # Create a mock assignment
    mock_assignment = Mock(spec=Assignment)
    mock_assignment.content = 'Valid content'
    mock_assignment.state = AssignmentStateEnum.DRAFT
    mock_assignment.student_id = 1

    # Mock get_by_id to return the mock assignment
    with patch('core.models.assignments.Assignment.get_by_id', return_value=mock_assignment), \
         patch('core.models.assignments.db.session.flush'):
        auth_principal = AuthPrincipal(student_id=1, teacher_id=1, user_id=1)
        assignment = Assignment.submit(1, 2, auth_principal)

    assert assignment.teacher_id == 2
    assert assignment.state == AssignmentStateEnum.DRAFT

def test_mark_grade(client, h_student_1):
    # Create a mock assignment
    mock_assignment = Mock(spec=Assignment)
    mock_assignment.state = AssignmentStateEnum.SUBMITTED
    mock_assignment.student_id = 1

    # Mock get_by_id to return the mock assignment
    with patch('core.models.assignments.Assignment.get_by_id', return_value=mock_assignment), \
         patch('core.models.assignments.db.session.flush'):
        auth_principal = AuthPrincipal(student_id=1, teacher_id=1, user_id=1)
        assignment = Assignment.mark_grade(1, GradeEnum.A, auth_principal)

    assert assignment.grade == GradeEnum.A
    assert assignment.state == AssignmentStateEnum.GRADED

def test_get_assignments_by_teacher(client):
    # Mock query.all to return a list of assignments
    with patch('core.models.assignments.Assignment.query') as mock_query:
        mock_query.all.return_value = [Assignment(id=1), Assignment(id=2)]
        assignments = Assignment.get_assignments_by_teacher()

        # Debugging information
        # print("Actual assignments:", assignments)

        assert len(assignments) == 2, f"Expected 2 assignments but got {len(assignments)}"

@pytest.fixture
def h_student_1():
    return {'X-Principal': '{"principal_id": 1, "user_id": 1, "student_id": 1, "teacher_id": 1}'}
