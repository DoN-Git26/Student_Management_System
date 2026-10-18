import pytest

from models.user import User
from utils import auth


def test_first_user_becomes_admin_then_roles_respected():
    first = auth.register("Grace", "Lee", "grace@example.com", "secret1", "student")
    assert first.role == "admin"
    second = auth.register("John", "Doe", "john@example.com", "secret1", "student")
    assert second.role == "student"
    with pytest.raises(auth.AuthError):
        auth.register("Evil", "User", "evil@example.com", "secret1", "admin")


def test_login_logout_session():
    auth.register("Grace", "Lee", "grace@example.com", "secret1")
    assert auth.current_user() is None
    with pytest.raises(auth.AuthError):
        auth.login("grace@example.com", "wrong")
    with pytest.raises(auth.AuthError):
        auth.login("nobody@example.com", "secret1")
    user = auth.login("GRACE@example.com", "secret1")
    assert auth.current_user() is user
    auth.logout()
    assert auth.current_user() is None
    auth.logout()
