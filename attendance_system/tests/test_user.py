import pytest

from models.student import Student
from models.user import User
from utils.security import hash_password, verify_password


def test_register_and_find_user():
    user = User.register_user("John", "Doe", "John@Example.com", "secret1", "student")
    assert isinstance(user, Student)
    assert User.find_user("john@example.com") is user
    assert user.get_full_name() == "John Doe"
    assert user.view_profile()["Role"] == "student"


def test_password_is_hashed_and_verified():
    user = User.register_user("John", "Doe", "j@example.com", "secret1", "student")
    assert "secret1" not in user.to_dict()["password_hash"]
    assert user.check_password("secret1")
    assert not user.check_password("wrong")


def test_hash_uses_random_salt():
    assert hash_password("abc123") != hash_password("abc123")
    assert not verify_password("abc123", "garbage")


@pytest.mark.parametrize("email", ["", "no-at-sign", "a@b"])
def test_invalid_email_rejected(email):
    with pytest.raises(ValueError):
        User("A", "B", email)


def test_duplicate_email_rejected():
    User("A", "B", "a@example.com")
    with pytest.raises(ValueError):
        User("C", "D", "A@example.com")


def test_short_password_and_bad_role_rejected():
    with pytest.raises(ValueError):
        User.register_user("A", "B", "a@example.com", "123", "student")
    with pytest.raises(ValueError):
        User.register_user("A", "B", "a@example.com", "secret1", "boss")
    assert User.all_users == []


def test_ids_increment_per_role():
    first = User.register_user("A", "B", "a@example.com", "secret1", "student")
    second = User.register_user("C", "D", "c@example.com", "secret1", "student")
    assert (first.user_id, second.user_id) == ("S001", "S002")


def test_roundtrip_dict():
    user = User.register_user("A", "B", "a@example.com", "secret1", "teacher")
    data = user.to_dict()
    User.all_users.clear()
    clone = User.from_dict(data)
    assert clone.role == "teacher" and clone.check_password("secret1")
