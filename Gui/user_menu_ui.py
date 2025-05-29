from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from Function.user_functions import UserFunctions

class UserMenuWindow(QWidget):
    def __init__(self, user_id, full_name):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle('ATM - User Menu')
        self.setFixedSize(500, 500)
        self.init_ui()
        self.update_balance()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.welcome_label = QLabel(f'Welcome, {self.full_name}')
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        
        self.balance_label = QLabel()
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet('font-size: 18px;')
        
        self.withdraw_button = QPushButton('Rút tiền')
        self.withdraw_button.clicked.connect(self.show_withdraw)
        
        self.deposit_button = QPushButton('Nạp tiền')
        self.deposit_button.clicked.connect(self.show_deposit)
        
        self.transfer_button = QPushButton('Gửi tiền')
        self.transfer_button.clicked.connect(self.show_transfer)
        
        self.change_pin_button = QPushButton('Đổi PIN')
        self.change_pin_button.clicked.connect(self.show_change_pin)
        
        self.history_button = QPushButton('Lịch sử giao dịch')
        self.history_button.clicked.connect(self.show_history)
        
        self.logout_button = QPushButton('Logout')
        self.logout_button.clicked.connect(self.logout)
        
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.withdraw_button)
        layout.addWidget(self.deposit_button)
        layout.addWidget(self.transfer_button)
        layout.addWidget(self.change_pin_button)
        layout.addWidget(self.history_button)
        layout.addWidget(self.logout_button)
        
        self.setLayout(layout)
    
    def update_balance(self):
        success, balance = UserFunctions.get_balance(self.user_id)
        if success:
            self.balance_label.setText(f'Số dư hiện tại: {balance:,.0f} VND')
        else:
            QMessageBox.warning(self, 'Error', balance)
    
    def show_withdraw(self):
        from Gui.withdraw_ui import WithdrawWindow
        self.withdraw_window = WithdrawWindow(self.user_id, self.full_name)
        self.withdraw_window.show()
        self.withdraw_window.balance_updated.connect(self.update_balance)
    
    def show_deposit(self):
        from Gui.deposit_ui import DepositWindow
        self.deposit_window = DepositWindow(self.user_id, self.full_name)
        self.deposit_window.show()
        self.deposit_window.balance_updated.connect(self.update_balance)
    
    def show_transfer(self):
        from Gui.transfer_ui import TransferWindow
        self.transfer_window = TransferWindow(self.user_id, self.full_name)
        self.transfer_window.show()
        self.transfer_window.balance_updated.connect(self.update_balance)
    
    def show_change_pin(self):
        from Gui.change_pin_ui import ChangePinWindow
        self.change_pin_window = ChangePinWindow(self.user_id, self.full_name)
        self.change_pin_window.show()
    
    def show_history(self):
        from Gui.history_ui import HistoryWindow
        self.history_window = HistoryWindow(self.user_id, self.full_name)
        self.history_window.show()
    
    def logout(self):
        from Gui.login_ui import LoginWindow
        self.hide()
        self.login_window = LoginWindow()
        self.login_window.show()