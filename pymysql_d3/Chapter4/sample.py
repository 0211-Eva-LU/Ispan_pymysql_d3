import pandas as pd
import pymysql
from configparser import ConfigParser


class Sample_Superstore():
    def __init__(self):
        # 讀取 csv 檔案
        self.df =pd.read_csv("Sample-Superstore.csv",encoding='latin-1')
        # 讀取 .env 檔案取得資料庫連線資訊
        config = ConfigParser()
        config.read('../Chapter1/config.ini')
        # 建立資料庫連線
        self.connection = pymysql.connect(
        host=config.get('DB', 'host'),
        user=config.get('DB', 'user'),
        password=config.get('DB', 'password'),
        port=config.getint('DB', 'port'),
        cursorclass=pymysql.cursors.DictCursor,
    )
        
    def create_database(self,databasename):
        with self.connection.cursor() as cursor:
        # 建立資料庫
            sql = "CREATE DATABASE IF NOT EXISTS %s"
            cursor.execute(sql,databasename)

            cursor.execute(f"SHOW DATABASES")
            dbs = cursor.fetchall()
            print(dbs)











