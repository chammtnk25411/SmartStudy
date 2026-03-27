class User:
    def __init__(self, id = None, name = None, username = None, email = None, password = None, role="user"):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def __str__(self):
        return f"{self.id}\t{self.name}\t{self.username}\t{self.email}\t{self.password}\t{self.role}"

