from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt

class AdminMenuWindow(QWidget):
    def __init__(self, user_id, full_name):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle('ATM - Admin Menu')
        self.setFixedSize(500, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.welcome_label = QLabel(f'Welcome Admin, {self.full_name}')
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        
        self.cash_deposit_button = QPushButton('Thêm tiền mặt vào ATM')
        self.cash_deposit_button.clicked.connect(self.show_cash_deposit)
        
        self.manage_users_button = QPushButton('Quản lý người người')
        self.manage_users_button.clicked.connect(self.show_manage_users)
        
        self.cash_balance_button = QPushButton('Xem số dư máy ATM')
        self.cash_balance_button.clicked.connect(self.show_cash_balance)
        
        self.transactions_button = QPushButton('Xem giao dịch')
        self.transactions_button.clicked.connect(self.show_all_transactions)
        
        self.logout_button = QPushButton('Đăng xuất')
        self.logout_button.clicked.connect(self.logout)
        
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.cash_deposit_button)
        layout.addWidget(self.manage_users_button)
        layout.addWidget(self.cash_balance_button)
        layout.addWidget(self.transactions_button)
        layout.addWidget(self.logout_button)
        
        self.setLayout(layout)
    
    def show_cash_deposit(self):
        from Gui.admin_deposit_ui import AdminDepositWindow
        self.deposit_window = AdminDepositWindow(self.user_id)
        self.deposit_window.show()
    
    def show_manage_users(self):
        from Gui.admin_manage_user_ui import AdminManageUserWindow
        self.manage_users_window = AdminManageUserWindow(self.user_id)
        self.manage_users_window.show()
    
    def show_cash_balance(self):
        from Gui.admin_cash_balance_ui import AdminCashBalanceWindow
        self.cash_balance_window = AdminCashBalanceWindow()
        self.cash_balance_window.show()
    
    def show_all_transactions(self):
        from Gui.admin_transaction_ui import AdminTransactionWindow
        self.transactions_window = AdminTransactionWindow()
        self.transactions_window.show()
    
    def logout(self):
        from Gui.login_ui import LoginWindow
        self.hide()
        self.login_window = LoginWindow()
        self.login_window.show()