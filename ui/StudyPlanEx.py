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

        # Set định dạng 24h cho QTimeEdit
        self.timeEdit_start.setDisplayFormat("HH:mm")
        self.timeEdit_end.setDisplayFormat("HH:mm")

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
        self.pushButtonUpdate.clicked.connect(self.processUpdate)
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
        self.pushButtonUpdate.setIcon(QIcon(get_path("images/update.png")))
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

    def calculate_total_time(self, start_time, end_time):
        start = QTime.fromString(start_time, "HH:mm")
        end = QTime.fromString(end_time, "HH:mm")

        # Nếu thời gian kết thúc nhỏ hơn thời gian bắt đầu (qua 12h đêm)
        if end < start:
            # Thêm 24 giờ (86400 giây) vào thời gian kết thúc
            total_seconds = start.secsTo(end) + 86400
        else:
            total_seconds = start.secsTo(end)

        return total_seconds // 60

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

            # Tính lại TotalTime để hiển thị
            total_time = self.calculate_total_time(p.StartTime, p.EndTime)
            self.tableWidgetPlan.setItem(row, 5, QTableWidgetItem(str(total_time)))

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

        # Kiểm tra xem có kế hoạch nào đang sử dụng topic này không
        plans_using_topic = []
        for p in self.lp.list:
            if p.PlanTopic == topic.TopicName and p.Username == self.currentUser:
                plans_using_topic.append(p.PlanName)

        if plans_using_topic:
            QMessageBox.warning(
                self.MainWindow,
                "Cảnh báo",
                f"Không thể xóa môn học '{topic.TopicName}' vì đang được sử dụng trong các kế hoạch:\n" +
                "\n".join(plans_using_topic)
            )
            return

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
        self.selectedPlan = None
        self.lineEdit_Name.setText("")
        self.comboBox.setCurrentIndex(0)
        self.dateEdit.setDate(QDate.currentDate())
        self.timeEdit_start.setTime(QTime(0, 0))
        self.timeEdit_end.setTime(QTime(0, 0))
        self.lineEdit_Name.setFocus()

    def validate_plan_data(self, plan_name, plan_topic):
        # Kiểm tra tính hợp lệ của dữ liệu kế hoạch
        if not plan_name or plan_name.strip() == "":
            QMessageBox.warning(self.MainWindow, "Cảnh báo", "Vui lòng nhập tên kế hoạch!")
            return False

        if not plan_topic or plan_topic == "":
            QMessageBox.warning(self.MainWindow, "Cảnh báo", "Vui lòng chọn môn học!")
            return False

        return True

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

        # Kiểm tra dữ liệu
        if not self.validate_plan_data(plan.PlanName, plan.PlanTopic):
            return

        # Tính tổng thời gian
        plan.TotalTime = self.calculate_total_time(plan.StartTime, plan.EndTime)

        # Kiểm tra nếu TotalTime = 0
        if plan.TotalTime == 0:
            reply = QMessageBox.question(
                self.MainWindow,
                "Xác nhận",
                "Thời gian học là 0 phút. Bạn có chắc muốn lưu kế hoạch này?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.lp.save_item(plan)
        plans_path = get_path("datasets/StudyPlans.json")
        self.lp.import_json(plans_path)
        self.display_plans()

        QMessageBox.information(self.MainWindow, "Thành công", "Đã thêm kế hoạch học mới!")
        self.processNew()

    def processUpdate(self):
        if self.selectedPlan is None:
            QMessageBox.warning(self.MainWindow, "Cảnh báo", "Vui lòng chọn kế hoạch cần cập nhật!")
            return

        # Lấy dữ liệu mới từ form
        updated_plan = Plan()
        updated_plan.PlanId = self.selectedPlan.PlanId
        updated_plan.PlanName = self.lineEdit_Name.text()
        updated_plan.PlanTopic = self.comboBox.currentText()
        updated_plan.Username = self.currentUser

        date = self.dateEdit.date()
        updated_plan.Date = date.toString("dd/MM/yyyy")

        start = self.timeEdit_start.time()
        end = self.timeEdit_end.time()

        updated_plan.StartTime = start.toString("HH:mm")
        updated_plan.EndTime = end.toString("HH:mm")

        # Kiểm tra dữ liệu
        if not self.validate_plan_data(updated_plan.PlanName, updated_plan.PlanTopic):
            return

        # Tính tổng thời gian
        updated_plan.TotalTime = self.calculate_total_time(updated_plan.StartTime, updated_plan.EndTime)

        # Xác nhận cập nhật
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận cập nhật",
            f"Bạn có chắc muốn cập nhật kế hoạch '{updated_plan.PlanName}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Lưu ID để xóa sau
            plan_id_to_update = self.selectedPlan.PlanId

            # Xóa kế hoạch cũ
            self.lp.remove_item(plan_id_to_update)
            # Thêm kế hoạch mới
            self.lp.save_item(updated_plan)
            # Reload dữ liệu
            plans_path = get_path("datasets/StudyPlans.json")
            self.lp.import_json(plans_path)
            self.display_plans()

            # Reset form SAU KHI đã hiển thị lại dữ liệu
            self.processNew()

            QMessageBox.information(self.MainWindow, "Thành công", "Đã cập nhật kế hoạch học!")

    def processRemove(self):
        if self.selectedPlan is None:
            QMessageBox.warning(self.MainWindow, "Cảnh báo", "Vui lòng chọn kế hoạch cần xóa!")
            return

        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa kế hoạch '{self.selectedPlan.PlanName}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Lưu ID để xóa
            plan_id_to_remove = self.selectedPlan.PlanId

            self.lp.remove_item(plan_id_to_remove)
            plans_path = get_path("datasets/StudyPlans.json")
            self.lp.import_json(plans_path)
            self.display_plans()

            # Reset form SAU KHI đã hiển thị lại dữ liệu
            self.processNew()

            QMessageBox.information(self.MainWindow, "Thành công", "Đã xóa kế hoạch học!")

    def processBack(self):
        if hasattr(self, 'main_window_ref') and self.main_window_ref:
            self.main_window_ref.reload_plans_and_check()
            self.main_window_ref.MainWindow.show()

        self.MainWindow.close()