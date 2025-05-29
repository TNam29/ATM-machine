from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from Function.user_functions import UserFunctions

class DepositWindow(QWidget):
    balance_updated = pyqtSignal()
    
    def __init__(self, user_id, full_name):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle('ATM - Gửi tiền')
        self.setFixedSize(600, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel(f'Gửi tiền - {self.full_name}')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        # Amount input
        self.amount_label = QLabel('Số lượng (tối thiểu là 10,000 VND):')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Nhập số tiền gửi')
        
        # Banknotes selection
        self.notes_group = QGroupBox("Chọn mệnh giá tiền gửi")
        notes_layout = QVBoxLayout()
        
        self.denominations = {
            500000: 0,
            200000: 0,
            100000: 0,
            50000: 0,
            20000: 0,
            10000: 0
        }
        
        self.note_inputs = {}
        
        for denom in sorted(self.denominations.keys(), reverse=True):
            hbox = QHBoxLayout()
            label = QLabel(f'{denom:,} VND:')
            spinbox = QLineEdit('0')
            spinbox.setFixedWidth(50)
            self.note_inputs[denom] = spinbox
            
            hbox.addWidget(label)
            hbox.addStretch()
            hbox.addWidget(spinbox)
            notes_layout.addLayout(hbox)
        
        self.notes_group.setLayout(notes_layout)
        
        # Buttons
        self.calculate_button = QPushButton('Calculate Total')
        self.calculate_button.clicked.connect(self.calculate_total)
        
        self.deposit_button = QPushButton('Gửi tiền')
        self.deposit_button.clicked.connect(self.handle_deposit)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.notes_group)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.deposit_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def calculate_total(self):
        total = 0
        deposit_notes = {}
        
        for denom, input_widget in self.note_inputs.items():
            try:
                count = int(input_widget.text())
                if count < 0:
                    QMessageBox.warning(self, 'Error', 'Count cannot be negative')
                    return
                deposit_notes[denom] = count
                total += denom * count
            except ValueError:
                QMessageBox.warning(self, 'Error', 'Please enter valid numbers')
                return
        
        self.amount_input.setText(str(total))
    
    def handle_deposit(self):
        amount_text = self.amount_input.text().strip()
        
        if not amount_text:
            QMessageBox.warning(self, 'Error', 'Please enter an amount')
            return
        
        try:
            amount = int(amount_text)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Amount must be a number')
            return
        
        if amount < 10000:
            QMessageBox.warning(self, 'Error', 'Minimum deposit is 10,000 VND')
            return
        
        deposit_notes = {}
        for denom, input_widget in self.note_inputs.items():
            try:
                count = int(input_widget.text())
                if count > 0:
                    deposit_notes[denom] = count
            except ValueError:
                pass
        
        success, result = UserFunctions.deposit(self.user_id, amount, deposit_notes)
        
        if success:
            QMessageBox.information(self, 'Success', 'Deposit completed successfully')
            self.balance_updated.emit()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result)