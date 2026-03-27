class Topic:
    def __init__(self, TopicId=None, TopicName=None,Username=None):
        self.TopicId = TopicId
        self.TopicName = TopicName
        self.Username = Username
    def __str__(self):
        infor=f'{self.TopicId}\t{self.TopicName}'
        return infor