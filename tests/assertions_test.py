from core.libs.assertions import (
    assert_auth,
    assert_true,
    assert_valid,
    assert_found
)
from core.libs.exceptions import FyleError

def test_assert_auth_success():
    # Assertion should not raise an error when condition is True
    assert_auth(True)

def test_assert_auth_failure():
    # Assertion should raise FyleError with status code 401 and default message 'UNAUTHORIZED'
    try:
        assert_auth(False)
    except FyleError as e:
        assert e.status_code == 401
        assert e.message == 'UNAUTHORIZED'

def test_assert_true_success():
    # Assertion should not raise an error when condition is True
    assert_true(True)

def test_assert_true_failure():
    # Assertion should raise FyleError with status code 403 and default message 'FORBIDDEN'
    try:
        assert_true(False)
    except FyleError as e:
        assert e.status_code == 403
        assert e.message == 'FORBIDDEN'

def test_assert_valid_success():
    # Assertion should not raise an error when condition is True
    assert_valid(True)

def test_assert_valid_failure():
    # Assertion should raise FyleError with status code 400 and default message 'BAD_REQUEST'
    try:
        assert_valid(False)
    except FyleError as e:
        assert e.status_code == 400
        assert e.message == 'BAD_REQUEST'

def test_assert_found_success():
    # Assertion should not raise an error when object is not None
    assert_found('object')

def test_assert_found_failure():
    # Assertion should raise FyleError with status code 404 and default message 'NOT_FOUND'
    try:
        assert_found(None)
    except FyleError as e:
        assert e.status_code == 404
        assert e.message == 'NOT_FOUND'
