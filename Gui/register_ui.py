from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from Function.user_functions import UserFunctions

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ATM - Register')
        self.setFixedSize(400, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Đăng ký tài khoản mới')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        
        self.password_label = QLabel('Password (6 ký tự):')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Nhập mật khẩu 6 ký tự')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.confirm_password_label = QLabel('Confirm Password:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Confirm your password')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        self.full_name_label = QLabel('Full Name:')
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText('Enter your full name')
        
        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.handle_register)
        
        self.back_button = QPushButton('Back to Login')
        self.back_button.clicked.connect(self.show_login)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.full_name_label)
        layout.addWidget(self.full_name_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        full_name = self.full_name_input.text().strip()
        
        if not all([username, password, confirm_password, full_name]):
            QMessageBox.warning(self, 'Error', 'All fields are required')
            return
        
        if len(password) != 6 or not password.isdigit():
            QMessageBox.warning(self, 'Error', 'Password must be 6 digits')
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return
        
        success, result = UserFunctions.register_user(username, password, full_name)
        
        if success:
            QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
            self.show_login()
        else:
            QMessageBox.warning(self, 'Error', result)
    
    def show_login(self):
        from Gui.login_ui import LoginWindow
        self.hide()
        self.login_window = LoginWindow()
        self.login_window.show()