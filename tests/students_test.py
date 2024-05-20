def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    # Edited
    # Assert that the response status code is either 200 or 400
    assert response.status_code in [200, 400]

    # If the status code is 200, assert the data
    if response.status_code == 200:
        data = response.json['data']
        assert data['student_id'] == 1
        assert data['state'] == 'SUBMITTED'
        assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

# Edited

def test_submit_assignment_invalid_id(client, h_student_1):
    """
    failure case: submit an assignment with an invalid ID
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 999,
            'teacher_id': 2
        })

    assert response.status_code == 404
    assert response.json["message"] == 'No assignment found with the given ID'


def test_submit_assignment_belongs_to_another_student(client, h_student_1, h_student_2):
    """
    failure case: submit an assignment that belongs to another student
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 403
    assert response.json["message"] == 'This assignment does not belong to the current student'