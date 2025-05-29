import pymysql

class DBConfig:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = '12345'
    DATABASE = 'atm_db'
    PORT = 3306

def get_db_connection():
    return pymysql.connect(
        host=DBConfig.HOST,
        user=DBConfig.USER,
        password=DBConfig.PASSWORD,
        database=DBConfig.DATABASE,
        port=DBConfig.PORT
    )