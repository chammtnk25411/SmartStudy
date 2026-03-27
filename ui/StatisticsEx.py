import json
import os
import sys
from datetime import date, datetime

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui.Statistics import Ui_MainWindow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class statistics_MainWindowEx(Ui_MainWindow):
    def __init__(self, username):
        super().__init__()
        self.currentUser = username
        self.current_view_date = date.today()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.SignalAndSlots()
        self.update_dashboard()

    def showWindow(self):
        self.MainWindow.show()
        bg = get_path("images/blue_bg.jpg")
        self.MainWindow.setStyleSheet(f"""
                        QMainWindow#MainWindow {{
                            border-image: url({bg}) 0 0 0 0 stretch stretch;
                        }}
                    """)
        frame = self.MainWindow.frameGeometry()
        center = self.MainWindow.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.MainWindow.move(frame.topLeft())

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def SignalAndSlots(self):
        self.pushButtonBefore.clicked.connect(self.load_past)
        self.pushButtonAfter.clicked.connect(self.load_future)
        self.pushButtonBack.clicked.connect(self.processBack)

    def load_past(self):
        self.current_view_date = date.fromordinal(self.current_view_date.toordinal() - 1)
        self.update_dashboard()

    def load_future(self):
        self.current_view_date = date.fromordinal(self.current_view_date.toordinal() + 1)
        self.update_dashboard()

    def calculate_statistics(self, view_date, username):
        view_year = view_date.year
        view_week = view_date.isocalendar()[1]

        planned_week_m = 0
        try:
            plans_path = get_path("datasets/StudyPlans.json")
            with open(plans_path, 'r', encoding='utf-8') as f:
                plans = json.load(f).get('datasets', [])
                for p in plans:
                    if p.get('Username', '').lower() == username.lower():
                        p_date_str = p.get('Date', '')
                        if p_date_str:
                            p_date = datetime.strptime(p_date_str, "%d/%m/%Y").date()
                            if p_date.year == view_year and p_date.isocalendar()[1] == view_week:
                                planned_week_m += int(p.get('TotalTime', 0))
        except Exception as e:
            print("Lỗi đọc Plans:", e)

        actual_today_m = 0
        actual_week_cumulative_m = 0
        actual_everyday_m = {i: 0 for i in range(7)}
        sub_today_m = {}
        try:
            history_path = get_path("datasets/history.json")
            with open(history_path, 'r', encoding='utf-8') as f:
                data_history = json.load(f)
                histories = data_history.get('datasets', data_history.get('danh_sach', []))
                for h in histories:
                    u = h.get('Username', h.get('username', ''))
                    status = h.get('Result', h.get('ket_qua', ''))
                    if str(u).lower() == username.lower() and status == 'Hoàn thành':
                        h_date_str = h.get('Date', h.get('ngay', '')).split()[0]
                        time_str = h.get('Duration', h.get('thoi_gian', ''))
                        sub_name = h.get('Subject', h.get('ten_mon', 'Tự học'))
                        if h_date_str and time_str:
                            try:
                                h_date = datetime.strptime(h_date_str, "%d/%m/%Y").date()
                                hour = 0
                                minute = 0
                                for part in time_str.split():
                                    if 'h' in part: hour = int(part.replace('h', ''))
                                    if 'm' in part: minute = int(part.replace('m', ''))
                                s_time = hour * 60 + minute
                                if h_date.year == view_year and h_date.isocalendar()[1] == view_week:
                                    actual_everyday_m[h_date.weekday()] += s_time
                                    if h_date <= view_date:
                                        actual_week_cumulative_m += s_time
                                    if h_date == view_date:
                                        actual_today_m += s_time
                                        sub_today_m[sub_name] = sub_today_m.get(sub_name, 0) + s_time
                            except:
                                pass
        except Exception as e:
            print("Lỗi đọc History:", e)

        percent = 0
        if planned_week_m > 0:
            percent = int(round((actual_week_cumulative_m / planned_week_m) * 100))
            if percent > 100:
                percent = 100
        return {
            'planned_week_h': round(planned_week_m / 60, 1),
            'actual_today_h': round(actual_today_m / 60, 1),
            'actual_week_cumulative_h': round(actual_week_cumulative_m / 60, 1),
            'percent': percent,
            'actual_everyday_h': [round(actual_everyday_m[i] / 60, 1) for i in range(7)],
            'sub_today_m': sub_today_m
        }

    def update_dashboard(self):
        str_ngay = self.current_view_date.strftime("%d/%m/%Y")
        self.labelDate.setText(f" Ngày đang xem: {str_ngay} ")
        today = date.today()
        self.pushButtonBefore.setEnabled(True)
        self.pushButtonAfter.setEnabled(self.current_view_date < today)
        res = self.calculate_statistics(self.current_view_date, self.currentUser)

        self.labelGoals.setText(
            f"Ngày này học được: {res['actual_today_h']} giờ\n"
            f"Tiến độ tuần (tính đến ngày này): {res['percent']}% ({res['actual_week_cumulative_h']}h / {res['planned_week_h']}h)"
        )
        if hasattr(self, 'progressBar'):
            self.progressBar.setValue(res['percent'])

        self.clearLayout(self.verticalLayoutAchievements)
        if not res['sub_today_m']:
            btn = QPushButton(text='Ngày này bạn chưa học môn nào cả!')
            self.style_display_button(btn)
            self.verticalLayoutAchievements.addWidget(btn)
        else:
            for sub_name, minute in res['sub_today_m'].items():
                hours = round(minute / 60, 1)
                btn = QPushButton(text=f'Môn: {sub_name}\nĐã học: {hours} giờ')
                self.style_display_button(btn)
                self.verticalLayoutAchievements.addWidget(btn)
        self.load_frequency(res['actual_everyday_h'])

    def style_display_button(self, btn):
        btn.setStyleSheet("""
            QPushButton {
                background-color: #E6E6E6;
                border: 1px solid #B4B4B4;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def load_frequency(self, actual_everyday_h):
        self.clearLayout(self.verticalLayoutPlots)
        fig = Figure(figsize=(5, 3), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        days = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        ax.bar(days, actual_everyday_h, color='#F0CA57', width=0.5, edgecolor='none')
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.set_ylabel('Số giờ (h)')
        self.verticalLayoutPlots.addWidget(canvas)
        canvas.draw()

    def processBack(self):
        if hasattr(self, 'main_window_ref') and self.main_window_ref:
            self.main_window_ref.show()
        self.MainWindow.close()