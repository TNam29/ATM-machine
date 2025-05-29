from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from Function.user_functions import UserFunctions

class WithdrawWindow(QWidget):
    balance_updated = pyqtSignal()
    
    def __init__(self, user_id, full_name):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle('ATM - Rút tiền')
        self.setFixedSize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel(f'Rút tiền - {self.full_name}')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.amount_label = QLabel('Số lượng (Bội số của 10,000 VND):')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Nhập số tiền muốn rút')
        
        self.withdraw_button = QPushButton('Rút')
        self.withdraw_button.clicked.connect(self.handle_withdraw)
        
        self.quick_buttons_layout = QHBoxLayout()
        self.quick_buttons = []
        amounts = [100000, 200000, 500000, 1000000, 2000000]
        
        for amount in amounts:
            btn = QPushButton(f'{amount:,} VND')
            btn.clicked.connect(lambda _, amt=amount: self.amount_input.setText(str(amt)))
            self.quick_buttons.append(btn)
            self.quick_buttons_layout.addWidget(btn)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addLayout(self.quick_buttons_layout)
        layout.addWidget(self.withdraw_button)
        layout.addWidget(self.result_text)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def handle_withdraw(self):
        amount_text = self.amount_input.text().strip()
        
        if not amount_text:
            QMessageBox.warning(self, 'Error', 'Please enter an amount')
            return
        
        try:
            amount = int(amount_text)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Amount must be a number')
            return
        
        success, result = UserFunctions.withdraw(self.user_id, amount)
        
        if success:
            notes_info = "Rút tiền thành công!\n\nSố tiền bạn nhận được:\n"
            for denom, count in result.items():
                notes_info += f"- {denom:,} VND x {count}\n"
            
            self.result_text.setPlainText(notes_info)
            self.balance_updated.emit()
        else:
            QMessageBox.warning(self, 'Error', result)