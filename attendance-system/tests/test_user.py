import pytest
from attendance_system.user import User

def test_register_and_find_user():
    user = User.register_user("John", "Doe", "john@example.com", "student")
    found = User.find_user("john@example.com")
    assert found == user
    assert found.get_full_name() == "John Doe"
    assert found.view_profile()["Role"] == "student"
