from PyQt5.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QHBoxLayout, QPushButton, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from Function.admin_functions import AdminFunctions

class AdminManageUserWindow(QWidget):
    def __init__(self, admin_id):
        super().__init__()
        self.admin_id = admin_id
        self.setWindowTitle('ATM - Quản lý người dùng')
        self.setFixedSize(900, 600)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel('Quản lý người dùng')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 20px; font-weight: bold;')
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Username', 'Full Name', 'Số dư', 'Admin', 'Thời gian'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton('Thêm người dùng')
        self.add_button.clicked.connect(self.show_add_user)
        
        self.edit_button = QPushButton('Chỉnh sửa người dùng')
        self.edit_button.clicked.connect(self.show_edit_user)
        
        self.delete_button = QPushButton('Xóa người dùng')
        self.delete_button.clicked.connect(self.delete_user)
        
        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.load_users)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.back_button)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_users(self):
        success, result = AdminFunctions.get_all_users()
        
        if success:
            self.table.setRowCount(len(result))
            
            for row_idx, user in enumerate(result):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(user['user_id'])))
                self.table.setItem(row_idx, 1, QTableWidgetItem(user['username']))
                self.table.setItem(row_idx, 2, QTableWidgetItem(user['full_name']))
                self.table.setItem(row_idx, 3, QTableWidgetItem(f"{user['balance']:,.0f} VND"))
                self.table.setItem(row_idx, 4, QTableWidgetItem('Yes' if user['is_admin'] else 'No'))
                self.table.setItem(row_idx, 5, QTableWidgetItem(user['created_at'].strftime('%Y-%m-%d %H:%M:%S')))
        else:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem('Error loading users'))
            self.table.setItem(0, 1, QTableWidgetItem(result))
    
    def show_add_user(self):
        from Gui.admin_add_user_ui import AdminAddUserWindow
        self.add_user_window = AdminAddUserWindow()
        self.add_user_window.user_added.connect(self.load_users)
        self.add_user_window.show()
    
    def show_edit_user(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Error', 'Xin chọn người dùng cần chỉnh sửa')
            return
        
        user_id = int(self.table.item(selected[0].row(), 0).text())
        username = self.table.item(selected[0].row(), 1).text()
        full_name = self.table.item(selected[0].row(), 2).text()
        is_admin = self.table.item(selected[0].row(), 4).text() == 'Yes'
        
        from Gui.admin_edit_user_ui import AdminEditUserWindow
        self.edit_user_window = AdminEditUserWindow(user_id, username, full_name, is_admin)
        self.edit_user_window.user_updated.connect(self.load_users)
        self.edit_user_window.show()
    
    def delete_user(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Error', 'Xin chọn người dùng cần xóa')
            return
        
        user_id = int(self.table.item(selected[0].row(), 0).text())
        username = self.table.item(selected[0].row(), 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Are you sure you want to delete user {username}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, result = AdminFunctions.delete_user(user_id)
            if success:
                QMessageBox.information(self, 'Success', 'User deleted successfully')
                self.load_users()
            else:
                QMessageBox.warning(self, 'Error', result)