from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, 
    QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from Function.admin_functions import AdminFunctions

class AdminAddUserWindow(QWidget):
    user_added = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ATM - Thêm người dùng')
        self.setFixedSize(400, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Thêm người dùng mới')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        
        self.password_label = QLabel('Password (6 kí tự):')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Nhập Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.full_name_label = QLabel('Full Name:')
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText('Nhập full name')
        
        self.is_admin_check = QCheckBox('Is Admin')
        
        self.add_button = QPushButton('Thêm người dùng')
        self.add_button.clicked.connect(self.handle_add_user)
        
        self.back_button = QPushButton('Hủy')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.full_name_label)
        layout.addWidget(self.full_name_input)
        layout.addWidget(self.is_admin_check)
        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def handle_add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        full_name = self.full_name_input.text().strip()
        is_admin = self.is_admin_check.isChecked()
        
        if not all([username, password, full_name]):
            QMessageBox.warning(self, 'Lỗi', 'Tất cả các ô không được để trống')
            return
        
        if len(password) != 6 or not password.isdigit():
            QMessageBox.warning(self, 'Lỗi', 'Mật khẩu phải có 6 kí tự')
            return
        
        success, result = AdminFunctions.add_user(username, password, full_name, is_admin)
        
        if success:
            QMessageBox.information(self, 'Thành công', 'Thêm người dùng thành công')
            self.user_added.emit()
            self.close()
        else:
            QMessageBox.warning(self, 'Lỗi', result)