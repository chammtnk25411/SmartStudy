import json
import os
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from PyQt6.QtCore import Qt
from ui.Rank import Ui_MainWindow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class Rank_MainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super().__init__()
        self.currentUser = username

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.setFixedSize(1070, 700)  # Khóa kích thước
        self.pushButtonBack.clicked.connect(self.processBack)
        self.load_top_10_leaderboard()

    def showWindow(self):
        self.MainWindow.show()
        self.pushButtonBack.setIcon(QIcon(get_path("images/back.jpg")))
        bg = get_path("images/blusky.png")
        self.MainWindow.setStyleSheet(f"""
                QMainWindow#MainWindow {{
                    border-image: url({bg}) 0 0 0 0 stretch stretch;
                }}
            """)
        frame = self.MainWindow.frameGeometry()
        center = self.MainWindow.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.MainWindow.move(frame.topLeft())

    def load_top_10_leaderboard(self):
        try:
            user_path = get_path("datasets/user.json")
            users = []
            if os.path.exists(user_path):
                with open(user_path, 'r', encoding='utf-8') as f:
                    users = json.load(f).get("users", [])
            user_scores = {u['username'].lower(): {"name": u['name'], "minutes": 0, "username": u['username']} for u in
                           users}

            history_path = get_path("datasets/history.json")
            if os.path.exists(history_path):
                with open(history_path, 'r', encoding='utf-8') as f:
                    data_history = json.load(f)
                    histories = data_history.get("datasets", data_history.get("danh_sach", []))
                    for h in histories:
                        status = h.get('Result', h.get('ket_qua', ''))
                        u = h.get('Username', h.get('username', '')).lower()
                        if status in ['Hoàn thành', 'Kết thúc sớm'] and u in user_scores:
                            time_str = h.get('Duration', h.get('thoi_gian', ''))
                            if time_str:
                                hour = 0
                                minute = 0
                                for part in time_str.split():
                                    if 'h' in part: hour = int(part.replace('h', ''))
                                    if 'm' in part: minute = int(part.replace('m', ''))
                                user_scores[u]["minutes"] += (hour * 60 + minute)
            active_users = [u for u in user_scores.values() if u["minutes"] > 0]
            active_users.sort(key=lambda x: x["minutes"], reverse=True)
            your_rank = 0
            your_hours = 0.0
            for index, user in enumerate(active_users):
                if user['username'].lower() == self.currentUser.lower():
                    your_rank = index + 1
                    your_hours = round(user["minutes"] / 60, 1)
                    break
            if hasattr(self, 'labelRankMe'):
                if your_rank > 0 and your_hours > 0:
                    self.labelRankMe.setText(f"🏅 Xếp hạng của bạn: TOP {your_rank} ({your_hours} giờ)")
                else:
                    self.labelRankMe.setText("🏅 Bạn chưa có dữ liệu học tập. Hãy bắt đầu học ngay!")
            if hasattr(self, 'listWidgetRank'):
                self.listWidgetRank.clear()
                for i in range(10):
                    rank = i + 1
                    if rank == 1:
                        medal = "🥇"
                    elif rank == 2:
                        medal = "🥈"
                    elif rank == 3:
                        medal = "🥉"
                    else:
                        medal = "⭐"
                    if i < len(active_users):
                        user = active_users[i]
                        hours = round(user["minutes"] / 60, 1)
                        display_text = f"{medal}\tTop {rank}\t{user['name']:<20}\tTổng: {hours:>5} giờ"
                        item = QListWidgetItem(display_text)
                    else:
                        display_text = f"{medal}\tTop {rank}\t------------------"
                        item = QListWidgetItem(display_text)
                        item.setForeground(Qt.GlobalColor.gray)
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
                    self.listWidgetRank.addItem(item)
        except Exception as e:
            print("Lỗi Load Bảng xếp hạng:", e)

    def processBack(self):
        if hasattr(self, 'main_window_ref') and self.main_window_ref:
            self.main_window_ref.show()
        self.MainWindow.close()