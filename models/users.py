import json

from models.mycollections import MyCollections
from models.user import User


class Users(MyCollections):

    def export_json(self, filename):
        self.filename = filename
        data = {'users': []}

        for item in self.list:
            data['users'].append({
                'id': item.id,
                'name': item.name,
                'username': item.username,
                'email': item.email,
                'password': item.password,
                'role': item.role
            })

        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()

        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)

            for item in data['users']:
                id = item["id"]
                name = item["name"]
                username = item["username"]
                email = item["email"]
                password = item["password"]
                role = item["role"]

                u = User(id, name, username, email, password, role)
                self.add_item(u)

    def find_item(self, u_id):
        u = None
        for it in self.list:
            if it.id == u_id:
                u = it
                break
        return u

    def save_item(self, u):
        exist_u = self.find_item(u.id)

        if exist_u == None:
            self.add_item(u)
        else:
            exist_u.id = u.id
            exist_u.name = u.name
            exist_u.username = u.username
            exist_u.email = u.email
            exist_u.password = u.password
            exist_u.role = u.role

        self.export_json(self.filename)

    def remove_item(self, u_id):
        u = self.find_item(u_id)

        if u == None:
            return False

        self.list.remove(u)
        self.export_json(self.filename)

        return True