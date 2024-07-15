
from core.models.assignments import AssignmentStateEnum, GradeEnum

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments', 
        headers=h_principal
        )
    assert response.status_code == 200
    
    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

def test_grade_submitted_assignment(client, h_principal):
    """
    Test case for grading a submitted assignment
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4, 'grade': GradeEnum.A.value},
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.A.value

def test_grade_draft_assignment(client, h_principal):
    """
    Test case for grading a draft assignment
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 5, 'grade': GradeEnum.A.value},
        headers=h_principal
    )
    assert response.status_code == 400

def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4, 'grade': GradeEnum.C.value},
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C.value

def test_grade_assignment_invalid_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4, 'grade': 'E'}, 
        headers=h_principal
    )
    assert response.status_code == 400

def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4, 'grade': 'B'},
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B.value
    
def test_list_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments', 
        headers=h_principal
    )
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

def test_list_assignments_for_non_existent_principal(client, h_principal):
    """
    Test case for listing assignments for a non-existent principal
    """
    response = client.get(
        '/principal/assignments', 
        headers={'Authorization': 'Bearer invalid_token'}
    )
    assert response.status_code == 401

    
def test_malformed_input_data(client, h_principal):
    """
    Test case for providing malformed input data
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'assignment_id': 4, 'grade_value': 'A'},
        headers=h_principal
    )
    assert response.status_code == 400
    
def test_list_teachers(client, h_principal):
    """
    Test case for listing teachers
    """
    response = client.get(
        '/principal/teachers', 
        headers=h_principal
    )
    assert response.status_code == 200
    data = response.json['data']
    assert isinstance(data, list)

def test_list_teachers_no_auth(client):
    """
    Test case for listing teachers without authentication
    """
    response = client.get('/principal/teachers')
    assert response.status_code == 401

def test_grade_assignment_missing_fields(client, h_principal):
    """
    Test case for grading an assignment with missing fields
    """
    response = client.post(
        '/principal/assignments/grade',
        json={'id': 4},
        headers=h_principal
    )
    assert response.status_code == 400