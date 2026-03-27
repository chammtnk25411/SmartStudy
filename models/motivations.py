import json
from models.motivation import Motivation
from models.mycollections import MyCollections


class Motivations(MyCollections):

    def export_json(self, filename):
        self.filename = filename
        data = {'datasets': []}

        for item in self.list:
            data['datasets'].append({
                'Id': item.Id,
                'Content': item.Content,
                'username': item.username
            })

        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()

        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)

            for item in data['datasets']:
                Id = item["Id"]
                Content = item["Content"]
                username = item.get("username")

                m = Motivation(Id, Content, username)
                self.add_item(m)
    def find_item(self, id):
        result = None
        for it in self.list:
            if it.Id == id:
                result = it
                break
        return result
    def save_item(self, motivation):
        exist = self.find_item(motivation.Id)
        if exist == None:
            self.add_item(motivation)
        else:
            exist.Id = motivation.Id
            exist.Content = motivation.Content
            exist.username = motivation.username
        self.export_json(self.filename)
    def remove_item(self, id):
        item = self.find_item(id)
        if item == None:
            return False
        self.list.remove(item)
        self.export_json(self.filename)
        return True

    def get_by_username(self, username):
        return [m for m in self.list if m.username == username]