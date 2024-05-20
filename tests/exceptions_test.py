from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    message = "Test error message"
    error = FyleError(404, message)
    assert error.status_code == 404
    assert error.message == message

def test_fyle_error_to_dict():
    message = "Test error message"
    error = FyleError(404, message)
    error_dict = error.to_dict()
    assert isinstance(error_dict, dict)
    assert 'message' in error_dict
    assert error_dict['message'] == message
