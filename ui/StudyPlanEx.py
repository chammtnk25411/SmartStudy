import json
import os
import sys
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QListWidgetItem, QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox, QInputDialog

from models.topic import Topic
from models.plan import Plan
from models.plans import Plans
from models.topics import Topics
from ui.StudyPlan import Ui_MainWindow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class StudyPlanEx(Ui_MainWindow):

    def __init__(self, username):
        super().__init__()

        self.currentUser = username

        topics_path = get_path("datasets/Topics.json")
        self.ltp = Topics()
        self.ltp.import_json(topics_path)

        plans_path = get_path("datasets/StudyPlans.json")
        self.lp = Plans()
        self.lp.import_json(plans_path)

        self.selectedPlan = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.MainWindow = MainWindow
        self.MainWindow.setFixedSize(self.MainWindow.width(), self.MainWindow.height())

        self.display_topics()
        self.display_plans()
        self.dateEdit.setDate(QDate.currentDate())

        self.setupSignalAndSlot()

        bg = get_path("images/may.jpg")
        self.MainWindow.setStyleSheet(f"""
                    QMainWindow {{
                        border-image: url({bg}) 0 0 0 0 stretch stretch;
                    }}
                """)

    def setupSignalAndSlot(self):
        self.pushButtonAddTopic.clicked.connect(self.processAddTopic)
        self.pushButton_deleteTopic.clicked.connect(self.processDeleteTopic)
        self.listWidgetTopic.itemClicked.connect(self.filter_plans_by_topic)
        self.tableWidgetPlan.cellClicked.connect(self.select_plan)
        self.pushButtonNew.clicked.connect(self.processNew)
        self.pushButtonSave.clicked.connect(self.processSave)
        self.pushButtonRemove.clicked.connect(self.processRemove)
        self.pushButtonBack.clicked.connect(self.processBack)

    def showWindow(self):
        self.MainWindow.show()
        frame = self.MainWindow.frameGeometry()
        center = self.MainWindow.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.MainWindow.move(frame.topLeft())

        self.pushButtonBack.setIcon(QIcon(get_path("images/back.jpg")))
        self.pushButtonAddTopic.setIcon(QIcon(get_path("images/plus.png")))
        self.pushButton_deleteTopic.setIcon(QIcon(get_path("images/bin.png")))
        self.pushButtonNew.setIcon(QIcon(get_path("images/plus.png")))
        self.pushButtonSave.setIcon(QIcon(get_path("images/save.png")))
        self.pushButtonRemove.setIcon(QIcon(get_path("images/bin.png")))

    def display_topics(self):
        self.listWidgetTopic.clear()
        self.comboBox.clear()

        for t in self.ltp.list:
            if t.Username.strip().lower() != self.currentUser.strip().lower():
                continue
            item = QListWidgetItem()
            item.setText(t.TopicName)
            item.setData(Qt.ItemDataRole.UserRole, t)
            self.listWidgetTopic.addItem(item)
            self.comboBox.addItem(t.TopicName)

    def display_plans(self):
        self.tableWidgetPlan.setRowCount(0)
        today = QDate.currentDate()
        for p in self.lp.list:
            if p.Username.strip().lower() != self.currentUser.strip().lower():
                continue
            row = self.tableWidgetPlan.rowCount()
            self.tableWidgetPlan.insertRow(row)
            self.tableWidgetPlan.setItem(row, 0, QTableWidgetItem(p.PlanTopic))
            self.tableWidgetPlan.setItem(row, 1, QTableWidgetItem(p.PlanName))
            self.tableWidgetPlan.setItem(row, 2, QTableWidgetItem(p.Date))
            self.tableWidgetPlan.setItem(row, 3, QTableWidgetItem(p.StartTime))
            self.tableWidgetPlan.setItem(row, 4, QTableWidgetItem(p.EndTime))
            self.tableWidgetPlan.setItem(row, 5, QTableWidgetItem(str(p.TotalTime)))

            try:
                d = p.Date.split("/")
                plan_date = QDate(int(d[2]), int(d[1]), int(d[0]))
                if plan_date < today:
                    for col in range(self.tableWidgetPlan.columnCount()):
                        item = self.tableWidgetPlan.item(row, col)
                        if item:
                            item.setBackground(Qt.GlobalColor.red)
            except:
                pass

    def generate_plan_id(self):
        max_id = 0
        for p in self.lp.list:
            try:
                num = int(p.PlanId[1:])
                if num > max_id:
                    max_id = num
            except:
                pass
        return "P" + str(max_id + 1)

    def processAddTopic(self):
        topic_name, ok = QInputDialog.getText(
            self.MainWindow,
            "Thêm Môn học",
            "Nhập tên Môn học:"
        )
        if not ok or topic_name.strip() == "":
            return
        topic_name = topic_name.strip()

        for t in self.ltp.list:
            if t.TopicName.lower() == topic_name.lower() and t.Username == self.currentUser:
                QMessageBox.warning(self.MainWindow, "Cảnh báo", "Môn học đã tồn tại!")
                return

        max_id = 0
        for t in self.ltp.list:
            try:
                num = int(t.TopicId[1:])
                if num > max_id:
                    max_id = num
            except:
                pass

        topic_id = "T" + str(max_id + 1)
        new_topic = Topic(topic_id, topic_name, self.currentUser)
        self.ltp.save_item(new_topic)

        topics_path = get_path("datasets/Topics.json")
        self.ltp.import_json(topics_path)
        self.display_topics()
        QMessageBox.information(self.MainWindow, "Thành công", "Đã thêm Môn học !")

    def processDeleteTopic(self):
        item = self.listWidgetTopic.currentItem()
        if item is None:
            QMessageBox.warning(self.MainWindow, "Cảnh báo", "Chọn Môn học để xóa!")
            return
        topic = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận",
            f"Bạn có chắc muốn xóa '{topic.TopicName}' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.ltp.remove_item(topic.TopicId)
            topics_path = get_path("datasets/Topics.json")
            self.ltp.import_json(topics_path)
            self.display_topics()

    def filter_plans_by_topic(self, item):
        topic_name = item.text().lower()
        index = self.comboBox.findText(item.text())
        if index >= 0:
            self.comboBox.setCurrentIndex(index)

        for row in range(self.tableWidgetPlan.rowCount()):
            topic_cell = self.tableWidgetPlan.item(row, 0)
            if topic_cell:
                if topic_name == topic_cell.text().lower():
                    for col in range(self.tableWidgetPlan.columnCount()):
                        cell = self.tableWidgetPlan.item(row, col)
                        if cell:
                            cell.setBackground(Qt.GlobalColor.green)
                else:
                    for col in range(self.tableWidgetPlan.columnCount()):
                        cell = self.tableWidgetPlan.item(row, col)
                        if cell:
                            cell.setBackground(Qt.GlobalColor.white)

    def select_plan(self, row, column):
        plan_name = self.tableWidgetPlan.item(row, 1).text()
        date = self.tableWidgetPlan.item(row, 2).text()

        for p in self.lp.list:
            if p.PlanName == plan_name and p.Date == date:
                self.selectedPlan = p
                self.lineEdit_Name.setText(p.PlanName)
                index = self.comboBox.findText(p.PlanTopic)
                if index >= 0:
                    self.comboBox.setCurrentIndex(index)
                d = p.Date.split("/")
                self.dateEdit.setDate(QDate(int(d[2]), int(d[1]), int(d[0])))
                st = p.StartTime.split(":")
                self.timeEdit_start.setTime(QTime(int(st[0]), int(st[1])))
                et = p.EndTime.split(":")
                self.timeEdit_end.setTime(QTime(int(et[0]), int(et[1])))
                break

    def processNew(self):
        self.lineEdit_Name.setText("")
        self.comboBox.setCurrentIndex(0)
        self.dateEdit.setDate(QDate.currentDate())
        self.selectedPlan = None
        self.lineEdit_Name.setFocus()

    def processSave(self):
        plan = Plan()
        plan.PlanId = self.generate_plan_id()
        plan.PlanName = self.lineEdit_Name.text()
        plan.PlanTopic = self.comboBox.currentText()
        plan.Username = self.currentUser
        date = self.dateEdit.date()
        plan.Date = date.toString("dd/MM/yyyy")
        start = self.timeEdit_start.time()
        end = self.timeEdit_end.time()
        plan.StartTime = start.toString("HH:mm")
        plan.EndTime = end.toString("HH:mm")
        plan.TotalTime = start.secsTo(end) // 60

        self.lp.save_item(plan)
        plans_path = get_path("datasets/StudyPlans.json")
        self.lp.import_json(plans_path)
        self.display_plans()

    def processRemove(self):
        if self.selectedPlan is None:
            return
        self.lp.remove_item(self.selectedPlan.PlanId)
        plans_path = get_path("datasets/StudyPlans.json")
        self.lp.import_json(plans_path)
        self.display_plans()

    def processBack(self):
        if hasattr(self, 'main_window_ref') and self.main_window_ref:
            self.main_window_ref.reload_plans_and_check()
            self.main_window_ref.MainWindow.show()
        self.MainWindow.close()