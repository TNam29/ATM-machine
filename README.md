1. Cài đặt môi trường:
      pip install PyQt5 pymysql
- PuQT5: thư viện giao diện
- pymysql : dùng để kết nối database với python
2. Khởi tạo cơ sở dữ liệu:( MySQL )
- Thực hiện mở MySQL và tạo MySQL database 
- Chạy file "init_db.sql" để tạo bảng và dữ liệu mẫu
3. Cấu hình database:
- Sửa file Database/db_config.py với thông tin kết nối cá nhân MySQL
4. Chạy ứng dụng:
python main.py

* Cấu trúc dự án:
- Database: Dữ liệu và cấu hình kết nối
- Function: Xử lý logic các chức năng
- GUI : giao diện

* Chức năng:
- Đăng ký ( có xác thực thông tin)
- Đăng nhập ( có xác thực thông tin, có phân quyền người dùng, phân quyền màn hình)
- Màn hình chính: Hiển thị thông tin người dùng
- Rút tiền  ( có thể tính cách thức thối tiền )
- Chuyển khoản
- Đổi mã PIN
- Nạp tiền ( nạp tiền theo cách lấy mệnh giá tờ tiền)
- Xem lịch sử giao dịch
- Admin có thể quản lý người dùng ( CRUD )
- Admin có thể nạp tiền vào máy
- Admin có thể xem số dư máy ATM
- Xem tất cả lịch sử thao tác trên máy ATM
