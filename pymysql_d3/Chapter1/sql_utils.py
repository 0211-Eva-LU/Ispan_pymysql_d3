# 引入所需套件

import pymysql

# 讀取 config.ini 檔案取得資料庫連線資訊
from configparser import ConfigParser
# 讀取 config.ini 檔案取得資料庫連線資訊

# 讀取 config.ini 檔案取得資料庫連線資訊

config = ConfigParser()
config.read('config.ini')



def show_databases():
    
    # 建立資料庫連線
    connection = pymysql.connect(
    host=config['DB']['host'],
    user=config['DB']['user'],
    password=config['DB']['password'],
    port=int(config['DB']['port']),
    cursorclass=pymysql.cursors.DictCursor,
    )

    with connection.cursor() as cursor:
    
        cursor.execute("SHOW DATABASES;")
        result = cursor.fetchall()
    
    return result





def sql_query(query):
    
    # 建立資料庫連線
    connection = pymysql.connect(
    host=config['DB']['host'],
    user=config['DB']['user'],
    password=config['DB']['password'],
    port=int(config['DB']['port']),
    cursorclass=pymysql.cursors.DictCursor,
    )
    with connection.cursor() as cursor:
        
        cursor.execute(query)
        result = cursor.fetchall()
    return result

show_databases()

