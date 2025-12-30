import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Passw0rd',
    database='web_scraping'
)

def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS store (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) UNIQUE,
                url TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                keyword VARCHAR(100),
                title VARCHAR(255),
                price VARCHAR(50),
                img_url TEXT,
                link TEXT,
                init_fetch_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                fetch_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                store_id INT,
                FOREIGN KEY (store_id) REFERENCES store(id),
                UNIQUE KEY unique_link (link(255))
            );
        """)

def insert_store_info(store_name, store_url):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO store (name, url) VALUES (%s, %s) ON DUPLICATE KEY UPDATE url=VALUES(url);", 
                       (store_name, store_url))
        r = cursor.rowcount
        print(r)
    connection.commit()

def insert_product_info(keyword, title, price, img_url, link, store_name):
    with connection.cursor() as cursor:
        # 取得 store_id
        cursor.execute("SELECT id FROM store WHERE name = %s;", (store_name,))
        store = cursor.fetchone()
        if store is None:
            print(f"Store '{store_name}' not found.")
            return
        store_id = store[0]

        # 插入產品資料
        cursor.execute("""
            INSERT INTO products (keyword, title, price, img_url, link, store_id) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE title=VALUES(title), price=VALUES(price), img_url=VALUES(img_url), fetch_at=CURRENT_TIMESTAMP;
        """, (keyword, title, price, img_url, link, store_id))
    connection.commit()


if __name__ == "__main__":
    create_table()
    insert_store_info("PChome 24h購物", "https://24h.pchome.com.tw/")
    insert_store_info("Momo", "https://www.momoshop.com.tw/main/Main.jsp")