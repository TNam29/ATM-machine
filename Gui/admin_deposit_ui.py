from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt
from Function.admin_functions import AdminFunctions

class AdminDepositWindow(QWidget):
    def __init__(self, admin_id):
        super().__init__()
        self.admin_id = admin_id
        self.setWindowTitle('ATM - Admin Gửi tiền')
        self.setFixedSize(600, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Gửi tiền vào ATM')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        # Banknotes selection
        self.notes_group = QGroupBox("Add Banknotes")
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
        self.deposit_button = QPushButton('Gửi tiền')
        self.deposit_button.clicked.connect(self.handle_deposit)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.notes_group)
        layout.addWidget(self.deposit_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def handle_deposit(self):
        deposit_notes = {}
        
        for denom, input_widget in self.note_inputs.items():
            try:
                count = int(input_widget.text())
                if count < 0:
                    QMessageBox.warning(self, 'Lỗi', 'Số tiền không thể âm')
                    return
                if count > 0:
                    deposit_notes[denom] = count
            except ValueError:
                QMessageBox.warning(self, 'Lỗi', 'Nhập số tiền hợp lệ')
                return
        
        if not deposit_notes:
            QMessageBox.warning(self, 'Error', 'Please add at least one banknote')
            return
        
        success, result = AdminFunctions.add_cash(deposit_notes)
        
        if success:
            QMessageBox.information(self, 'Thành công', 'Nạp tiền thành công')
            self.close()
        else:
            QMessageBox.warning(self, 'Error', result)
            