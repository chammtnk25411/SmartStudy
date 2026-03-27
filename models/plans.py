import json

from models.mycollections import MyCollections
from models.plan import Plan


class Plans(MyCollections):

    def export_json(self, filename):
        self.filename = filename
        data = {'datasets': []}

        for item in self.list:
            data['datasets'].append({
                'PlanId': item.PlanId,
                'PlanName': item.PlanName,
                'PlanTopic': item.PlanTopic,
                'Date': item.Date,
                'StartTime': item.StartTime,
                'EndTime': item.EndTime,
                'TotalTime': item.TotalTime,
                'Username' : item.Username
            })

        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()

        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)

            for item in data['datasets']:
                PlanId = item['PlanId']
                PlanName = item['PlanName']
                PlanTopic = item['PlanTopic']
                Date = item['Date']
                StartTime = item['StartTime']
                EndTime = item['EndTime']
                TotalTime = item['TotalTime']
                Username = item['Username']

                plan = Plan(PlanId, PlanName, PlanTopic, Date, StartTime, EndTime, TotalTime, Username)
                self.add_item(plan)

    def find_item(self, planId):
        plan = None
        for item in self.list:
            if item.PlanId == planId:
                plan = item
                break
        return plan

    def save_item(self, plan):
        # Kiểm tra plan đã tồn tại chưa
        exist_plan = self.find_item(plan.PlanId)

        if exist_plan is None:
            # thêm mới
            self.add_item(plan)
        else:
            # cập nhật
            exist_plan.PlanName = plan.PlanName
            exist_plan.PlanTopic = plan.PlanTopic
            exist_plan.Date = plan.Date
            exist_plan.StartTime = plan.StartTime
            exist_plan.EndTime = plan.EndTime
            exist_plan.TotalTime = plan.TotalTime
            exist_plan.Username = plan.Username

        # lưu lại file json
        self.export_json(self.filename)

    def remove_item(self, planId):
        plan = self.find_item(planId)

        if plan is None:
            return False

        self.list.remove(plan)
        self.export_json(self.filename)
        return True