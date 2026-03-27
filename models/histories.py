import os
import json
from models.mycollections import MyCollections
from models.history import History


class Histories(MyCollections):

    def export_json(self, filename):
        self.filename = filename
        data = {'datasets': []}

        for item in self.list:
            data['datasets'].append({
                'HistoryId': item.HistoryId,
                'Username': item.Username,
                'Session': item.phien_so,
                'Date': item.ngay,
                'Duration': item.thoi_gian,
                'Result': item.ket_qua,
                'Subject': item.ten_mon
            })

        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def import_json(self, filename):
        self.filename = filename
        self.list.clear()

        if not os.path.exists(filename):
            return

        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)

            for item in data['datasets']:
                HistoryId = item.get("HistoryId")
                Username = item.get("Username")
                phien_so = item.get("Session")
                ngay = item.get("Date")
                thoi_gian = item.get("Duration")
                ket_qua = item.get("Result")
                ten_mon = item.get("Subject")

                h = History(HistoryId, Username, phien_so, ngay, thoi_gian, ket_qua, ten_mon)
                self.add_item(h)

    def find_item(self, id):
        result = None
        for it in self.list:
            if it.HistoryId == id:
                result = it
                break
        return result

    def save_item(self, history):
        exist_history = self.find_item(history.HistoryId)
        if exist_history == None:
            self.add_item(history)
        else:
            exist_history.HistoryId = history.HistoryId
            exist_history.Username = history.Username
            exist_history.phien_so = history.phien_so
            exist_history.ngay = history.ngay
            exist_history.thoi_gian = history.thoi_gian
            exist_history.ket_qua = history.ket_qua
            exist_history.ten_mon = history.ten_mon
        self.export_json(self.filename)

    def remove_item(self, id):
        item = self.find_item(id)
        if item == None:
            return False
        self.list.remove(item)
        self.export_json(self.filename)
        return True

    def get_tong_thoi_gian_hoc(self, username):
        tong_phut = 0
        for item in self.list:
            if item.Username == username and item.ket_qua == "Hoàn thành":
                pass
        return tong_phut

    def get_max_phien_so_trong_ngay(self, username, today):
        max_phien = 0
        for item in self.list:
            if item.Username == username and item.ngay.startswith(today):
                phien = int(item.phien_so)
                if phien > max_phien:
                    max_phien = phien
        return max_phien