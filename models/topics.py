import json
from models.mycollections import MyCollections
from models.topic import Topic


class Topics (MyCollections):
    def export_json(self, filename):
        self.filename = filename
        data = {'datasets': []}
        for item in self.list:
            data['datasets'].append({
            'TopicId': item.TopicId,
            'TopicName': item.TopicName,
            'Username': item.Username
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()
        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)
            for item in data['datasets']:
                TopicId = item["TopicId"]
                TopicName = item["TopicName"]
                Username = item["Username"]
                if TopicName is None:
                    TopicName = ""
                c = Topic(TopicId, TopicName, Username)
                self.add_item(c)

    def find_item(self, id):
        result = None
        for it in self.list:
            if it.TopicId == id:
                result = it
                break
        return result

    def save_item(self, topic):
        # Bước 1: Kiểm tra đối tượng tp có tồn tại trong kho không:
        exist_tp = self.find_item(topic.TopicId)
        # Bước 2: Nếu exist_tp=None--> thêm mới
        if exist_tp == None:  # xử lý thêm mới với điều kiện này
            self.add_item(topic)  # thêm nối đuôi tài sản mới vào cuối danh sách
        else:  # Xử lý cập nhật với điều kiện này (exist_tp !=None)
        # ta sửa dữ liệu trên ô nhớ:
            exist_tp.TopicId = topic.TopicId
            exist_tp.TopicName = topic.TopicName
            exist_tp.Username= topic.Username
            # Bước 3: Export dữ liệu từ bộ nhớ ra ổ cứng để lưu lại
        self.export_json(self.filename)

    def remove_item(self, id):
        # Bước 1: Tìm tài sản tpId này có tồn tại trong kho không
        tp = self.find_item(id)
        # Bước 2: nếu tồn tại thì xóa:
        if tp == None:
            return False
        self.list.remove(tp)
        # Bước 3: Export dữ liệu từ bộ nhớ ra ổ cứng để lưu lại:
        self.export_json(self.filename)
        return True