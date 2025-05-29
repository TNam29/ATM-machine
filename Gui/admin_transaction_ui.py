from PyQt5.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QHeaderView, QPushButton
)
from PyQt5.QtCore import Qt
from Function.admin_functions import AdminFunctions

class AdminTransactionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ATM - Giao dịch')
        self.setFixedSize(1000, 600)
        self.init_ui()
        self.load_transactions()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Tất cả giao dịch')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Loại', 'Số lượng', 'Người gửi', 'Người nhận', 'Thời gian'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.table)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
    
    def load_transactions(self):
        success, result = AdminFunctions.get_all_transactions()
        
        if success:
            self.table.setRowCount(len(result))
            
            for row_idx, transaction in enumerate(result):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(transaction['transaction_id'])))
                self.table.setItem(row_idx, 1, QTableWidgetItem(transaction['type']))
                
                amount = transaction['amount']
                if amount is not None:
                    self.table.setItem(row_idx, 2, QTableWidgetItem(f'{amount:,.0f} VND'))
                else:
                    self.table.setItem(row_idx, 2, QTableWidgetItem('N/A'))
                
                self.table.setItem(row_idx, 3, QTableWidgetItem(
                    f"{transaction['sender_name']} ({transaction['sender_username']})"
                ))
                
                if transaction['recipient_name']:
                    self.table.setItem(row_idx, 4, QTableWidgetItem(
                        f"{transaction['recipient_name']} ({transaction['recipient_username']})"
                    ))
                else:
                    self.table.setItem(row_idx, 4, QTableWidgetItem('N/A'))
                
                self.table.setItem(row_idx, 5, QTableWidgetItem(
                    transaction['date'].strftime('%Y-%m-%d %H:%M:%S')
                ))
        else:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem('Error loading transactions'))
            self.table.setItem(0, 1, QTableWidgetItem(result))