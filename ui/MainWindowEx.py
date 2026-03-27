import sys
import random
import os

from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6.QtCore import QTimer, Qt, QDateTime
from ui.MainWindow import Ui_MainWindow
from models.motivations import Motivations
from ui.MotivationEx import MotivationEx
from ui.RankEx import Rank_MainWindowEx
from ui.StatisticsEx import statistics_MainWindowEx
from ui.StudyPlanEx import StudyPlanEx
from ui.timerEx import SmartStudyTimer
from models.plans import Plans

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class MainWindowEx(Ui_MainWindow):
    def __init__(self, username):
        super().__init__()
        plans_path = get_path("datasets/StudyPlans.json")
        self.plans = Plans()
        self.plans.import_json(plans_path)
        self.currentUser = username
        self.motivations = Motivations()
        self.json_path = get_path("datasets/motivations.json")

        if os.path.exists(self.json_path):
            try:
                self.motivations.import_json(self.json_path)
            except Exception as e:
                print(f"Lỗi nạp dữ liệu: {e}")
        self.study_plan_win = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.check_upcoming_plan()
        self.MainWindow = MainWindow
        self.timer_plan = QTimer(self.MainWindow)
        self.timer_plan.timeout.connect(self.check_upcoming_plan)
        self.timer_plan.start(1000)
        self.pushButtonTimetable.clicked.connect(self.open_study_plan)
        self.pushButtonClock.clicked.connect(self.open_timer)
        self.pushButtonRank.clicked.connect(self.open_Rank)
        self.pushButtonStatistic.clicked.connect(self.open_statistic)

        bg = get_path("images/mwin.png")
        self.MainWindow.setStyleSheet(f"""
        QMainWindow{{
            border-image: url({bg});
        }}
        #centralwidget{{
            background: transparent;
        }}
        QPushButton{{
            background-color: rgba(255,255,255,200);
            border-radius:15px;
            border:1px solid rgba(255,255,255,120);
            color:black;
            font-weight:bold;
        }}
        QPushButton:hover{{
            background-color: rgba(255,255,255,230);
            border:2px solid #4aa3ff;
        }}
        QPushButton:pressed{{
            background-color: rgba(200,220,255,200);
        }}
        QPushButton#pushButtonMotivation{{
            background-color: rgba(255,255,255,220);
            color: rgb(26,116,172);
            font-size:25px;
            border-radius:20px;
        }}
        """)

        self.pushButtonStatistic.setIcon(QIcon(get_path("images/target.png")))
        self.pushButtonRank.setIcon(QIcon(get_path("images/ic_target.png")))
        self.pushButtonExit.setIcon(QIcon(get_path("images/ic_exit.png")))
        self.pushButtonTimetable.setIcon(QIcon(get_path("images/ic_schedule.png")))
        self.pushButtonClock.setIcon(QIcon(get_path("images/ic_clock.png")))

        self.pushButtonStatistic.setIconSize(QtCore.QSize(50, 50))
        self.pushButtonRank.setIconSize(QtCore.QSize(50, 50))
        self.pushButtonExit.setIconSize(QtCore.QSize(50, 50))
        self.pushButtonTimetable.setIconSize(QtCore.QSize(40, 40))
        self.pushButtonClock.setIconSize(QtCore.QSize(40, 40))

        self.show_random_motivation()
        self.timer = QTimer(self.MainWindow)
        self.timer.timeout.connect(self.show_random_motivation)
        self.timer.start(3000)

        self.pushButtonExit.clicked.connect(QApplication.instance().quit)
        self.pushButtonMotivation.clicked.connect(self.open_motivation_window)

    def showWindow(self):
        self.MainWindow.show()
        frame = self.MainWindow.frameGeometry()
        center = self.MainWindow.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.MainWindow.move(frame.topLeft())

    def open_study_plan(self):
        self.study_plan_window = QMainWindow()
        self.study_plan_ui = StudyPlanEx(self.currentUser)
        self.study_plan_ui.setupUi(self.study_plan_window)
        self.study_plan_ui.main_window_ref = self
        self.study_plan_window.show()
        self.MainWindow.hide()

    def open_timer(self):
        self.timer_window = SmartStudyTimer(self.currentUser)
        self.timer_window.main_window_ref = self.MainWindow
        self.timer_window.show()
        self.MainWindow.hide()

    def show_random_motivation(self):
        user_motivations = self.motivations.get_by_username(self.currentUser)
        if user_motivations:
            m = random.choice(user_motivations)
            self.pushButtonMotivation.setText(str(m.Content))

    def check_upcoming_plan(self):
        now = QDateTime.currentDateTime()
        found = False
        for p in self.plans.list:
            if p.Username.strip().lower() != self.currentUser.strip().lower():
                continue
            try:
                d = p.Date.split("/")
                t = p.StartTime.split(":")
                plan_time = QDateTime(
                    int(d[2]), int(d[1]), int(d[0]),
                    int(t[0]), int(t[1])
                )
                t_end = p.EndTime.split(":")
                end_time = QDateTime(
                    int(d[2]), int(d[1]), int(d[0]),
                    int(t_end[0]), int(t_end[1])
                )
                diff = now.secsTo(plan_time)

                if plan_time <= now <= end_time:
                    time_left = now.secsTo(end_time)
                    minutes = time_left // 60
                    seconds = time_left % 60
                    self.lblNotification.setText(
                        f"ĐANG HỌC: {p.PlanTopic} - {p.PlanName}\nCòn {minutes} phút {seconds:02d} giây"
                    )
                    self.lblNotification.setStyleSheet(
                        "background-color: green; color: white; font-weight: bold;"
                    )
                    found = True
                    break
                if 0 < diff <= 600:
                    minutes = diff // 60
                    seconds = diff % 60
                    time_left = f"{minutes} phút {seconds:02d} giây"
                    self.lblNotification.setText(
                        f"Sắp tới: {p.PlanTopic} - {p.PlanName} ({p.StartTime})\nCòn {time_left}"
                    )
                    self.lblNotification.setStyleSheet(
                        "background-color: blue; color: yellow; font-weight: bold;"
                    )
                    found = True
                    break
                elif -300 <= diff <= 0:
                    self.lblNotification.setText(
                        f"ĐÃ ĐẾN GIỜ: {p.PlanTopic} - {p.PlanName}"
                    )
                    self.lblNotification.setStyleSheet(
                        "background-color: red; color: white; font-weight: bold;"
                    )
                    if not hasattr(self, "notified") or self.notified != p.PlanId:
                        QMessageBox.information(
                            self.MainWindow,
                            "Thông báo",
                            f"Đã đến giờ học:\n{p.PlanTopic} - {p.PlanName}"
                        )
                        self.notified = p.PlanId
                    found = True
                    break
            except:
                pass

        if not found:
            self.lblNotification.setText("Không có lịch sắp tới")
            self.lblNotification.setStyleSheet(
                "background-color: white; color: black;"
            )

    def open_motivation_window(self):
        self.motivation_win = MotivationEx(self.currentUser)
        self.motivation_win.data_changed.connect(self.reload_motivation)
        self.motivation_win.main_window_ref = self.MainWindow
        self.motivation_win.show()
        self.MainWindow.hide()

    def open_statistic(self):
        self.statistic_window = QMainWindow()
        self.statistic_ui = statistics_MainWindowEx(self.currentUser)
        self.statistic_ui.setupUi(self.statistic_window)
        self.statistic_ui.main_window_ref = self.MainWindow
        self.statistic_ui.showWindow()
        self.MainWindow.hide()

    def open_Rank(self):
        self.rank_window = QMainWindow()
        self.rank_ui = Rank_MainWindowEx(self.currentUser)
        self.rank_ui.setupUi(self.rank_window)
        self.rank_ui.main_window_ref = self.MainWindow
        self.rank_ui.showWindow()
        self.MainWindow.hide()

    def reload_motivation(self):
        self.motivations.import_json(self.json_path)
        self.show_random_motivation()

    def reload_plans_and_check(self):
        plans_path = get_path("datasets/StudyPlans.json")
        self.plans.import_json(plans_path)
        self.check_upcoming_plan()