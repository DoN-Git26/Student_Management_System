class User:
    all_users = []

    def __init__(self, first_name, last_name, email, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        User.all_users.append(self)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def view_profile(self):
        return {
            "Name": self.get_full_name(),
            "Email": self.email,
            "Role": self.role
        }

    @classmethod
    def register_user(cls, first_name, last_name, email, role):
        return cls(first_name, last_name, email, role)

    @classmethod
    def find_user(cls, email):
        return next((u for u in cls.all_users if u.email == email), None)
