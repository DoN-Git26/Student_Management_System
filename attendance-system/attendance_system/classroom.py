class Classroom:
    all_classes = []

    def __init__(self, class_id, class_name, teacher):
        self.class_id = class_id
        self.class_name = class_name
        self.teacher = teacher
        self.students = []
        Classroom.all_classes.append(self)

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        self.students.remove(student)

    def get_student_list(self):
        return [s.get_full_name() for s in self.students]
