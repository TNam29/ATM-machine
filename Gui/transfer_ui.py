from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from Function.user_functions import UserFunctions

class TransferWindow(QWidget):
    balance_updated = pyqtSignal()
    
    def __init__(self, user_id, full_name):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle('ATM - Chuyển tiền')
        self.setFixedSize(500, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel(f'Chuyển tiền - {self.full_name}')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.recipient_label = QLabel('Username người nhận:')
        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText('Nhập username người nhận')
        
        self.amount_label = QLabel('Số lượng:')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Nhập số lượng muốn gửi')
        
        self.transfer_button = QPushButton('Gửi')
        self.transfer_button.clicked.connect(self.handle_transfer)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.recipient_label)
        layout.addWidget(self.recipient_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.transfer_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def handle_transfer(self):
        recipient = self.recipient_input.text().strip()
        amount_text = self.amount_input.text().strip()
        
        if not recipient or not amount_text:
            QMessageBox.warning(self, 'Error', 'Please fill all fields')
            return
        
        try:
            amount = int(amount_text)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Amount must be a number')
            return
        
        if amount <= 0:
            QMessageBox.warning(self, 'Error', 'Amount must be positive')
            return
        
        success, result = UserFunctions.transfer(self.user_id, recipient, amount)
        
        if success:
            QMessageBox.information(self, 'Success', 'Transfer completed successfully')
            self.balance_updated.emit()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result)