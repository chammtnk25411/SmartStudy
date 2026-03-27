import os
import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow

from ui.timer import Ui_MainWindow
from models.topics import Topics
from models.histories import Histories
from models.history import History

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class SmartStudyTimer(QMainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.currentUser = username

        self.file_name_history = get_path("datasets/history.json")
        topic_path = get_path("datasets/Topics.json")

        self.is_break_mode = False
        self.thoi_gian_goc = "0h 0m 0s"
        self.tong_phut_da_nhap = 0
        self.time_left = 0
        self.gio_goc = 0
        self.phut_goc = 0
        self.giay_goc = 0

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.topics_manager = Topics()
        self.topics_manager.import_json(topic_path)
        self.load_topics_to_combo()

        self.history_manager = Histories()
        self.history_manager.import_json(self.file_name_history)

        today = QtCore.QDateTime.currentDateTime().toString("dd/MM/yyyy")
        self.phien_hoc = self.history_manager.get_max_phien_so_trong_ngay(self.currentUser, today)
        self.ui.lbl_session.setText(f"{self.phien_hoc}")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self._setup_ui_elements()
        self._connect_signals()

    def load_topics_to_combo(self):
        self.ui.combo_subject.clear()
        for topic in self.topics_manager.list:
            if topic.Username == self.currentUser:
                self.ui.combo_subject.addItem(topic.TopicName, topic.TopicId)

    def set_ui_locked(self, locked: bool):
        state = not locked
        widgets = [self.ui.spinBox, self.ui.spinBox_2, self.ui.spinBox_3, self.ui.combo_subject]
        for widget in widgets:
            widget.setEnabled(state)

    def _setup_ui_elements(self):
        bg_timer_path = get_path("images/background.timer.jpg")
        bg_path = get_path("images/bg.png")
        start_path = get_path("images/start.png")
        pause_path = get_path("images/pause.png")
        finish_path = get_path("images/finish.qrc.png")
        exit_path = get_path("images/exit.png")

        self.setStyleSheet(f"""
            QMainWindow {{
                border-image: url('{bg_timer_path}') 0 0 0 0 stretch stretch;
            }}
        """)
        self.ui.frame.setStyleSheet(f"border-image: url('{bg_path}');")
        self.ui.btn_start.setStyleSheet(f"border-image: url('{start_path}');")
        self.ui.btn_pause.setStyleSheet(f"border-image: url('{pause_path}');")
        self.ui.btn_stop.setStyleSheet(f"border-image: url('{finish_path}');")
        self.ui.btn_exit.setStyleSheet(f"border-image: url('{exit_path}');")

        for spinbox in (self.ui.spinBox, self.ui.spinBox_2, self.ui.spinBox_3):
            spinbox.raise_()
            spinbox.setMaximum(9999)
            spinbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def _connect_signals(self):
        self.ui.btn_start.clicked.connect(self.start_timer)
        self.ui.btn_pause.clicked.connect(self.pause_timer)
        self.ui.btn_stop.clicked.connect(self.stop_timer)
        self.ui.btn_exit.clicked.connect(self.processBack)

    def save_history(self, trang_thai):
        if self.is_break_mode:
            return

        self.phien_hoc += 1
        self.ui.lbl_session.setText(f"{self.phien_hoc}")

        ten_mon_hoc = self.ui.combo_subject.currentText()
        if not ten_mon_hoc:
            ten_mon_hoc = "Tự học"

        date_time_now = QtCore.QDateTime.currentDateTime()
        ngay_id = date_time_now.toString("ddMMyyyy")
        chuoi_ngay_gio = date_time_now.toString("dd/MM/yyyy HH:mm")

        new_id = f"{self.currentUser}_{ngay_id}_phien{self.phien_hoc}"

        new_session = History(
            HistoryId=new_id,
            Username=self.currentUser,
            phien_so=self.phien_hoc,
            ngay=chuoi_ngay_gio,
            thoi_gian=self.thoi_gian_goc,
            ket_qua=trang_thai,
            ten_mon=ten_mon_hoc
        )
        self.history_manager.save_item(new_session)

    def update_break_time_json(self, phut_nghi):
        pass

    def start_timer(self):
        if not self.timer.isActive():
            if self.time_left == 0:
                gio = self.ui.spinBox.value()
                phut = self.ui.spinBox_2.value()
                giay = self.ui.spinBox_3.value()
                self.gio_goc = gio
                self.phut_goc = phut
                self.giay_goc = giay
                self.tong_phut_da_nhap = (gio * 60) + phut
                self.thoi_gian_goc = f"{gio}h {phut}m {giay}s"
                self.time_left = (gio * 3600) + (phut * 60) + giay

                if self.time_left == 0:
                    QtWidgets.QMessageBox.warning(self, "Lỗi", "Bạn chưa nhập thời gian!")
                    return

                self.set_ui_locked(True)
                self.update_spinbox_display()
            self.timer.start(1000)

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def stop_timer(self):
        if self.timer.isActive() or self.time_left > 0:
            self.timer.stop()
            self.set_ui_locked(False)

            if not self.is_break_mode:
                self.save_history("Kết thúc sớm")

            self.is_break_mode = False
            self.time_left = 0
            self.update_spinbox_display()
            self.ui.spinBox.setValue(self.gio_goc)
            self.ui.spinBox_2.setValue(self.phut_goc)
            self.ui.spinBox_3.setValue(self.giay_goc)
            QtWidgets.QMessageBox.information(self, "Kết thúc", "Đã dừng phiên học!")

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_spinbox_display()
        else:
            self.timer.stop()
            if not self.is_break_mode:
                self.save_history("Hoàn thành")
                QtWidgets.QMessageBox.information(self, "Hoàn thành",
                                                  f"Chúc mừng bạn đã xong phiên thứ {self.phien_hoc}!")
                if self.tong_phut_da_nhap >= 40:
                    hoi_nghi = QtWidgets.QMessageBox.question(
                        self, "Nghỉ ngơi",
                        "Bạn có muốn nghỉ 10 phút không?",
                        QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
                    )
                    if hoi_nghi == QtWidgets.QMessageBox.StandardButton.Yes:
                        self.is_break_mode = True
                        self.time_left = 10 * 60
                        self.update_break_time_json(10)
                        self.set_ui_locked(True)
                        self.update_spinbox_display()
                        self.timer.start(1000)
                    else:
                        self.set_ui_locked(False)
                        self.ui.spinBox.setValue(self.gio_goc)
                        self.ui.spinBox_2.setValue(self.phut_goc)
                        self.ui.spinBox_3.setValue(self.giay_goc)
                else:
                    self.set_ui_locked(False)
                    self.ui.spinBox.setValue(self.gio_goc)
                    self.ui.spinBox_2.setValue(self.phut_goc)
                    self.ui.spinBox_3.setValue(self.giay_goc)
            else:
                self.is_break_mode = False
                self.set_ui_locked(False)
                self.time_left = 0
                self.update_spinbox_display()
                QtWidgets.QMessageBox.information(self, "Hết giờ nghỉ", "Quay lại học thôi!")
                self.ui.spinBox.setValue(self.gio_goc)
                self.ui.spinBox_2.setValue(self.phut_goc)
                self.ui.spinBox_3.setValue(self.giay_goc)

    def update_spinbox_display(self):
        gio = self.time_left // 3600
        phut = (self.time_left % 3600) // 60
        giay = self.time_left % 60
        self.ui.spinBox.setValue(gio)
        self.ui.spinBox_2.setValue(phut)
        self.ui.spinBox_3.setValue(giay)

    def processBack(self):
        if hasattr(self, 'main_window_ref') and self.main_window_ref:
            self.main_window_ref.show()
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        self.close()