import json
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QVBoxLayout
from ui.admain import Ui_MainWindow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class AdminMainWindowEx(Ui_MainWindow):
    def __init__(self, username="admin"):
        super().__init__()
        self.currentUser = username
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.setFixedSize(self.MainWindow.width(), self.MainWindow.height())
        central_widget = self.MainWindow.centralWidget()
        if central_widget is not None:
            layout = central_widget.layout()
            if layout is None:
                layout = QVBoxLayout(central_widget)
                layout.addWidget(self.tableWidget)
            layout.setContentsMargins(80, 60, 80, 60)

        bg = get_path("images/galaxy.jpg")
        self.MainWindow.setStyleSheet(f"""
        QMainWindow {{
            border-image: url({bg}) 0 0 0 0 stretch stretch;
        }}

        QTableWidget {{
            background-color: white;  /* Đổi thành màu trắng đục */
            color: black;
            border: 1px solid #cccccc;
            border-radius: 10px;
            gridline-color: #e0e0e0;
            alternate-background-color: #f9f9f9;
        }}

        QTableWidget::item {{
            background-color: white;  /* Đổi item thành nền trắng */
            color: black;
        }}

        QTableWidget::item:selected {{
            background-color: #3498db;
            color: white;
        }}

        QHeaderView::section {{
            background-color: rgba(40, 40, 40, 220);
            color: white;
            font-weight: bold;
            border: none;
            padding: 6px;
        }}

        QTableCornerButton::section {{
            background-color: rgba(40, 40, 40, 220);
            border: none;
        }}
        """)

        self.setup_table()
        self.load_and_show_data()
    def showWindow(self):
        self.MainWindow.show()

    def setup_table(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)

        self.tableWidget.setEditTriggers(self.tableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(self.tableWidget.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(self.tableWidget.SelectionMode.SingleSelection)
        self.tableWidget.verticalHeader().setVisible(False)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

    def load_json_data(self, file_path, key):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(key, [])
        except Exception as e:
            print("Lỗi đọc file:", file_path, e)
            return []

    def parse_duration_to_minutes(self, duration_text):
        if not duration_text:
            return 0
        hour = 0
        minute = 0
        parts = duration_text.split()
        for p in parts:
            if "h" in p:
                try:
                    hour = int(p.replace("h", ""))
                except:
                    hour = 0
            elif "m" in p:
                try:
                    minute = int(p.replace("m", ""))
                except:
                    minute = 0
        return hour * 60 + minute

    def load_and_show_data(self):
        user_path = get_path("datasets/user.json")
        history_path = get_path("datasets/history.json")
        plans_path = get_path("datasets/StudyPlans.json")

        real_users = self.load_json_data(user_path, "users")
        real_histories = self.load_json_data(history_path, "datasets")
        real_plans = self.load_json_data(plans_path, "datasets")

        real_users_filtered = []
        for u in real_users:
            if u.get("role", "") != "admin":
                real_users_filtered.append(u)

        user_info_dict = {}
        for u in real_users_filtered:
            username = u.get("username", "")
            user_info_dict[username] = {
                "id": str(u.get("id", "")),
                "name": u.get("name", ""),
                "email": u.get("email", ""),
                "username": username,
                "password": u.get("password", ""),
                "so_phien": 0,
                "tong_phut_hoc": 0,
                "tong_phut_muc_tieu": 0
            }

        for h in real_histories:
            username = h.get("Username", "")
            duration = h.get("Duration", "0h 0m 0s")
            result = h.get("Result", "")
            if username in user_info_dict:
                user_info_dict[username]["so_phien"] += 1
                if result in ["Hoàn thành", "Kết thúc sớm"]:
                    so_phut = self.parse_duration_to_minutes(duration)
                    user_info_dict[username]["tong_phut_hoc"] += so_phut

        for p in real_plans:
            username = p.get("Username", "")
            if username in user_info_dict:
                try:
                    thoi_gian_ke_hoach = int(p.get("TotalTime", 0))
                except:
                    thoi_gian_ke_hoach = 0
                user_info_dict[username]["tong_phut_muc_tieu"] += thoi_gian_ke_hoach

        sorted_by_time = sorted(
            user_info_dict.values(),
            key=lambda x: x["tong_phut_hoc"],
            reverse=True
        )

        rank_map = {}
        rank = 1
        for u in sorted_by_time:
            if u["tong_phut_hoc"] > 0:
                rank_map[u["username"]] = rank
                rank += 1

        sorted_users_by_id = sorted(
            user_info_dict.values(),
            key=lambda x: int(x["id"]) if x["id"].isdigit() else 999999
        )

        self.tableWidget.setRowCount(0)
        row = 0

        for u in sorted_users_by_id:
            username = u["username"]
            self.tableWidget.insertRow(row)
            thu_hang = rank_map.get(username, "Chưa xếp hạng")
            muc_tieu_str = f"{u['tong_phut_muc_tieu']} phút" if u['tong_phut_muc_tieu'] > 0 else "0 phút"

            data = [
                u["id"],
                u["name"],
                u["email"],
                u["username"],
                u["password"],
                str(u["so_phien"]),
                muc_tieu_str,
                str(thu_hang)
            ]

            for col in range(len(data)):
                item = QTableWidgetItem(data[col])
                if col == 1:
                    item.setToolTip(data[col])
                if col in [0, 5, 6, 7]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.tableWidget.setItem(row, col, item)
            row += 1