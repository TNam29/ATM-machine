from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from Function.user_functions import UserFunctions

class ChangePinWindow(QWidget):
    def __init__(self, user_id, full_name):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle('ATM - Đổi mã PIN')
        self.setFixedSize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel(f'Đổi mã PIN - {self.full_name}')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.new_pin_label = QLabel('PIN mới (6 ký tự):')
        self.new_pin_input = QLineEdit()
        self.new_pin_input.setPlaceholderText('Nhập PIN mới:')
        self.new_pin_input.setEchoMode(QLineEdit.Password)
        self.new_pin_input.setMaxLength(6)
        
        self.confirm_pin_label = QLabel('Xác nhận PIN:')
        self.confirm_pin_input = QLineEdit()
        self.confirm_pin_input.setPlaceholderText('Xác nhận PIN mới')
        self.confirm_pin_input.setEchoMode(QLineEdit.Password)
        self.confirm_pin_input.setMaxLength(6)
        
        self.change_button = QPushButton('Đổi PIN')
        self.change_button.clicked.connect(self.handle_change_pin)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.new_pin_label)
        layout.addWidget(self.new_pin_input)
        layout.addWidget(self.confirm_pin_label)
        layout.addWidget(self.confirm_pin_input)
        layout.addWidget(self.change_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def handle_change_pin(self):
        new_pin = self.new_pin_input.text().strip()
        confirm_pin = self.confirm_pin_input.text().strip()
        
        if not new_pin or not confirm_pin:
            QMessageBox.warning(self, 'Error', 'Please fill all fields')
            return
        
        if len(new_pin) != 6 or not new_pin.isdigit():
            QMessageBox.warning(self, 'Error', 'PIN must be 6 digits')
            return
        
        if new_pin != confirm_pin:
            QMessageBox.warning(self, 'Error', 'PINs do not match')
            return
        
        success, result = UserFunctions.change_pin(self.user_id, new_pin)
        
        if success:
            QMessageBox.information(self, 'Success', 'PIN changed successfully')
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result)