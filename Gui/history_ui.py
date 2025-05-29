from PyQt5.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QHeaderView, QPushButton
)
from PyQt5.QtCore import Qt
from Function.user_functions import UserFunctions

class HistoryWindow(QWidget):
    def __init__(self, user_id, full_name):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle('ATM - Lịch sử giao dịch')
        self.setFixedSize(800, 500)
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel(f'Lịch sử giao dịch - {self.full_name}')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Loại', 'Số lượng', 'Người nhận', 'Thời gian'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.table)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def load_history(self):
        success, result = UserFunctions.get_transaction_history(self.user_id)
        
        if success:
            self.table.setRowCount(len(result))
            
            for row_idx, transaction in enumerate(result):
                self.table.setItem(row_idx, 0, QTableWidgetItem(transaction['type']))
                
                amount = transaction['amount']
                if amount is not None:
                    self.table.setItem(row_idx, 1, QTableWidgetItem(f'{amount:,.0f} VND'))
                else:
                    self.table.setItem(row_idx, 1, QTableWidgetItem('N/A'))
                
                self.table.setItem(row_idx, 2, QTableWidgetItem(transaction['recipient'] or 'N/A'))
                self.table.setItem(row_idx, 3, QTableWidgetItem(transaction['date'].strftime('%Y-%m-%d %H:%M:%S')))
        else:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem('Error loading history'))
            self.table.setItem(0, 1, QTableWidgetItem(result))