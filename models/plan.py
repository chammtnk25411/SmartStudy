class Plan:

    def __init__(self, PlanId=None, PlanName=None, PlanTopic=None,
                 Date=None, StartTime=None, EndTime=None,
                 TotalTime=None, Username=None):

        self.PlanId = PlanId
        self.PlanName = PlanName
        self.PlanTopic = PlanTopic
        self.Date = Date
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.TotalTime = TotalTime
        self.Username = Username

    def __str__(self):
        return f"{self.PlanId}\t{self.PlanName}\t{self.PlanTopic}\t{self.Date}\t{self.StartTime}\t{self.EndTime}\t{self.TotalTime}"