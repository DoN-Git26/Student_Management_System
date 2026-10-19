"""Administrator subclass."""

from models.attendance import Attendance
from models.classroom import Classroom
from models.user import User

EDITABLE_FIELDS = {"first_name", "last_name", "email"}


class Administrator(User):
    """An administrator who manages users, classes and reports."""

    ROLE = "admin"
    PREFIX = "A"

    @property
    def admin_id(self):
        return self.user_id

    def add_user(self, user):
        """Make sure a user is in the registry (no duplicates)."""
        if user not in User.all_users:
            User.all_users.append(user)

    def update_user(self, user, **fields):
        """Update a user's name or email."""
        unknown = set(fields) - EDITABLE_FIELDS
        if unknown:
            raise ValueError(f"Cannot update: {', '.join(sorted(unknown))}.")
        for key, value in fields.items():
            setattr(user, key, value)

    def remove_user(self, user):
        """Remove a student or teacher along with their links and records."""
        if user.role == "admin":
            raise ValueError("Administrator accounts cannot be removed.")
        if user.role == "teacher" and user.assigned_classes:
            raise ValueError("Reassign or remove this teacher's classes first.")
        if user.role == "student":
            for classroom in user.enrolled_classes:
                classroom.remove_student(user)
            Attendance.remove_for_student(user)
        User.all_users.remove(user)

    def create_class(self, class_id, class_name, teacher):
        """Create a classroom."""
        return Classroom(class_id, class_name, teacher)

    def view_all_attendance(self):
        """Return every attendance record."""
        return list(Attendance.all_records)

    def generate_report(self):
        """Return attendance details for all records."""
        return [r.get_attendance_details() for r in Attendance.all_records]
