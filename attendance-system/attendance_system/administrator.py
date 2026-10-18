from attendance_system.user import User
from attendance_system.classroom import Classroom

class Administrator(User):
    def __init__(self, first_name, last_name, email, admin_id):
        super().__init__(first_name, last_name, email, "admin")
        self.admin_id = admin_id

    def add_student(self, student):
        User.all_users.append(student)

    def update_student(self, student, **kwargs):
        for key, value in kwargs.items():
            setattr(student, key, value)

    def remove_student(self, student):
        User.all_users.remove(student)

    def create_class(self, class_id, class_name, teacher):
        return Classroom(class_id, class_name, teacher)

    def view_all_attendance(self):
        from attendance_system.attendance import Attendance
        return Attendance.all_records

    def generate_report(self):
        from attendance_system.attendance import Attendance
        return [rec.get_attendance_details() for rec in Attendance.all_records]
