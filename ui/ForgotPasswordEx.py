
import json
import os
import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.ForgotPassword import Ui_MainWindow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_helper import get_path


class ForgotPasswordEx(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupSignalAndSlot()
        self.setFixedSize(self.width(), self.height())
    def showWindow(self):
        bg = get_path("images/premain.png")
        self.setStyleSheet(f"""
                QMainWindow{{
                    border-image: url({bg});
                }}
            """)
        self.show()
        frame = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def setupSignalAndSlot(self):
        self.ui.pushButtonXacNhan.clicked.connect(self.process_reset_password)
        self.ui.back.mousePressEvent = self.open_login

    def process_reset_password(self):
        username = self.ui.lineEditUserName.text()
        email = self.ui.lineEditEmail.text()
        new_password = self.ui.lineEditPassWord.text()

        if username == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập Username")
            return
        if email == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập Email")
            return
        if new_password == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mật khẩu mới")
            return

        reply = QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc muốn đổi mật khẩu mới không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        try:
            user_path = get_path("datasets/user.json")
            with open(user_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                users = data["users"]

            found = False
            for user in users:
                if user["username"] == username and user["email"] == email:
                    user["password"] = new_password
                    found = True
                    break

            if not found:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy tài khoản")
                return

            with open(user_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            QMessageBox.information(self, "Thành công", "Đổi mật khẩu thành công!")
            self.ui.lineEditUserName.clear()
            self.ui.lineEditEmail.clear()
            self.ui.lineEditPassWord.clear()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def open_login(self, event):
        from ui.LoginEx import LoginEx
        from PyQt6.QtWidgets import QMainWindow

        self.login_window = QMainWindow()
        self.ui_login = LoginEx()
        self.ui_login.setupUi(self.login_window)
        self.login_window.show()
        self.close()