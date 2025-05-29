from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from Function.user_functions import UserFunctions

class LoginWindow(QWidget):    # kế thừa lớp cơ sở của cửa sổ QT5
    def __init__(self):        # constructor, tham chiếu cho object gui
        super().__init__()
        self.setWindowTitle('ATM - Login')
        self.setFixedSize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('ATM Login')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)
        
        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.show_register)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Cần nhập cả username và password')
            return
        
        success, result = UserFunctions.authenticate_user(username, password)
        
        if success:
            from Gui.user_menu_ui import UserMenuWindow
            from Gui.admin_menu_ui import AdminMenuWindow
            
            self.hide()
            
            if result['is_admin']:
                self.admin_window = AdminMenuWindow(result['user_id'], result['full_name'])
                self.admin_window.show()
            else:
                self.user_window = UserMenuWindow(result['user_id'], result['full_name'])
                self.user_window.show()
        else:
            QMessageBox.warning(self, 'Error', result)
    
    def show_register(self):
        from Gui.register_ui import RegisterWindow
        self.hide()
        self.register_window = RegisterWindow()
        self.register_window.show()