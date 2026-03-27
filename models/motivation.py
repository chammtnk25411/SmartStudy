class Motivation:
    def __init__(self, Id=None, Content=None, username=None):
        self.Id = Id
        self.Content = Content
        self.username = username
    def __str__(self):
        return f'{self.Id}\t{self.Content}\t{self.username}'