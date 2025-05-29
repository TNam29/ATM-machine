from PyQt5.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QHeaderView, QPushButton
)
from PyQt5.QtCore import Qt
from Function.admin_functions import AdminFunctions

class AdminCashBalanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ATM - Số dư tiền mặt')
        self.setFixedSize(500, 400)
        self.init_ui()
        self.load_cash_balance()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('ATM Số dư tiền mặt')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Mệnh giá', 'Số lượng'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.total_label = QLabel()
        self.total_label.setAlignment(Qt.AlignRight)
        self.total_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.table)
        layout.addWidget(self.total_label)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def load_cash_balance(self):
        success, result = AdminFunctions.get_cash_balance()
        
        if success:
            self.table.setRowCount(len(result['banknotes']))
            
            for row_idx, (denom, quantity) in enumerate(result['banknotes'].items()):
                self.table.setItem(row_idx, 0, QTableWidgetItem(f'{denom:,} VND'))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(quantity)))
            
            self.total_label.setText(f'Total: {result["total"]:,.0f} VND')
        else:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem('Error loading cash balance'))
            self.table.setItem(0, 1, QTableWidgetItem(result))