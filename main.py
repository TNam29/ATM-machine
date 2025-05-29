import sys
from PyQt5.QtWidgets import QApplication
from Gui.login_ui import LoginWindow
from Database.db_config import get_db_connection

def main():
    # ket noi csdl
    try:
        conn = get_db_connection()
        conn.close()
    except Exception as e:
        print(f"Database connection error: {e}")
        sys.exit(1)

    # run
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())   # vòng lặp cho đến khi end

if __name__ == "__main__":
    main()