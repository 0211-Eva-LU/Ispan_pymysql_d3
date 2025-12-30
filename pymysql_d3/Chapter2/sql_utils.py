import pymysql
import configparser 

config = configparser.ConfigParser()
config.read('../Chapter1/config.ini')


class MySQLManager():

    def __init__(self,database):
        # 建立資料庫連線
        self.connection = pymysql.connect(
        host=config['DB']['host'],
        user=config['DB']['user'],
        password=config['DB']['password'],
        port=int(config['DB']['port']),
        cursorclass=pymysql.cursors.DictCursor,
        database=database
        )



    def sql_query(self,query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            r = cursor.fetchall()
        return r
    

    # 查詢使用者的 function

    def get_user_info(self,username,password):
        with self.connection.cursor() as cursor:
            sql = """
                SELECT * FROM users WHERE username = %s AND password = %s
                """
            
            cursor.execute(sql,(username,password))
            r = cursor.fetchall()
        
        return r


# create_user_table()

    def screate_user_table(self):
        with self.connection.cursor() as cursor:

            sql = """
                CREATE TABLE IF NOT EXISTS users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
                )
                """
            cursor.execute(sql)
        print("資料表建立完成")

    


#update_password()

    def update_password(self,username,password):
        try:
            with self.connection.cursor() as cursor:

                sql = """
                    UPDATE users SET password = %s , WHERE username = %s;
                    """
                cursor.execute(sql,(password,username))
        except :
            print("發生錯誤取消更動")
            self.connection.rollback()
        finally:
            self.connection.commit()
            print("更新資料完成")        
           

#delete_user()



    def delete_user(self,username,password):
            try:
                with self.connection.cursor() as cursor:

                    sql = """
                        DELETE users WHERE username = %s AND password =  %s;
                        """
                    cursor.execute(sql,(username,password))
            except :
                print("發生錯誤取消更動")
                self.connection.rollback()
            finally:
                self.connection.commit()
                print("刪除資料完成")        
            

# 建立寫入使用者的 function

    def add_user(self,name,age,username,password):
            
        with self.connection.cursor() as cursor:

            sql = """
                INSERT INTO users(name,age,username,password)
                VALUES
                (%s, %s, %s, %s)
                """
            try:
                cursor.execute(sql,(name,age,username,password))
            except pymysql.err.IntegrityError as e :
                print(f"{username}已被使用")
                return
            
            if cursor.rowcount == 1:
                print("資料建立完成") 
            else:
                print("使用者未建立")
        
        self.connection.commit()



        
                