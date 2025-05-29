from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, 
    QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from Function.admin_functions import AdminFunctions

class AdminEditUserWindow(QWidget):
    user_updated = pyqtSignal()
    
    def __init__(self, user_id, username, full_name, is_admin):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle('ATM - Chỉnh sửa người dùng')
        self.setFixedSize(400, 400)
        self.init_ui(username, full_name, is_admin)
    
    def init_ui(self, username, full_name, is_admin):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Chỉnh sửa người dùng')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(username)
        
        self.full_name_label = QLabel('Full Name:')
        self.full_name_input = QLineEdit(full_name)
        
        self.is_admin_check = QCheckBox('Is Admin')
        self.is_admin_check.setChecked(is_admin)
        
        self.update_button = QPushButton('Cập nhật người dùng')
        self.update_button.clicked.connect(self.handle_update_user)
        
        self.back_button = QPushButton('Hủy')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.full_name_label)
        layout.addWidget(self.full_name_input)
        layout.addWidget(self.is_admin_check)
        layout.addWidget(self.update_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def handle_update_user(self):
        username = self.username_input.text().strip()
        full_name = self.full_name_input.text().strip()
        is_admin = self.is_admin_check.isChecked()
        
        if not all([username, full_name]):
            QMessageBox.warning(self, 'Error', 'All fields are required')
            return
        
        success, result = AdminFunctions.update_user(
            self.user_id, username, full_name, is_admin
        )
        
        if success:
            QMessageBox.information(self, 'Thành công', 'Cập nhật người dùng thành công')
            self.user_updated.emit()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result)