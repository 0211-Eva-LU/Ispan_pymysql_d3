# pymysql_d3
[PyMySQL Connection Object](#pymysql-connection-object) | [PyMySQL Cursor Object](#pymysql-cursor-object) | [configparser 常用方法與屬性](#configparser-常用方法與屬性) | 

### 安裝本專案所需套件
```
pip install -r requirements.txt
```

### 建立連線
```python
import pymysql

connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    cursorclass=cursors.DictCursor # 使用字典游標
)
```

### PyMySQL Connection Object
> `pymysql.connect()` 呼叫後返回的物件，用於管理資料庫連線和事務。

| 常用 | 名稱 | 說明 |
| :---: | :--- | :--- |
| V | `cursor()` | **建立並返回一個游標物件**（Cursor Object），用於執行 SQL 語句。 |
| V | `commit()` | 提交當前事務（Transaction）的所有更改到資料庫。 |
|  | `rollback()` | **回溯**（Undo）當前事務的所有更改，取消尚未提交的操作。 |
| V | `close()` | 關閉資料庫連線。建議使用 `with` 語句來自動處理。 |
|  | `autocommit` | 布林值，設定是否自動提交事務。`True` 為自動提交（預設為 `False`）。 |
|  | `host` | 連線到的資料庫主機名稱。 |
|  | `db` | 連線到的資料庫名稱。 |

### PyMySQL Cursor Object
> 由 `Connection.cursor()` 返回的物件，用於執行 SQL 語句並處理結果集。

| 常用 | 名稱 | 說明 |
| :---: | :--- | :--- |
| V | `execute(sql[, args])` | **執行一條 SQL 語句**。`args` 是可選的參數序列，用於安全地傳遞變數。 |
| | `executemany(sql, args_list)` | **執行多條相似的 SQL 語句**。`args_list` 是一個參數序列的列表。 |
| | `fetchone()` | **從結果集中取出一行**（Tuple）資料。如果沒有資料則返回 `None`。 |
| | `fetchmany([size])` | **從結果集中取出多行資料**。`size` 預設為 `cursor.arraysize` 的值。 |
| V | `fetchall()` | **從結果集中取出所有行資料**（Tuple 的列表）。 |
| | `close()` | 關閉游標物件。 |
| V | `rowcount` | 上一個 `execute()` **影響或匹配的行數**。例如 `INSERT`、`UPDATE`、`DELETE` 或 `SELECT` 的行數。 |
| | `lastrowid` | 對於 `INSERT` 操作，返回最後一個插入行的 **主鍵 ID**（如果主鍵是自動增長的）。 |
| | `description` | 包含結果集欄位（Columns）資訊的序列（如果為 `SELECT` 語句）。 |
| | `arraysize` | 設定 `fetchmany()` 每次返回的行數（預設為 1）。 |

### configparser 常用方法與屬性
| 類別 | 方法/屬性 | 描述 |
| :--- | :--- | :--- |
| **I. 核心管理** | `read(filenames)` | 讀取並解析一個或多個 INI 檔案，返回成功讀取的檔案列表。 |
| | `write(fileobject)` | 將配置資料寫入檔案物件（例如 `open()` 的結果）。 |
| | `sections()` | 取得所有非預設區段名稱的列表。 |
| | `add_section(name)` | 新增一個區段。 |
| | `remove_section(name)` | 移除一個區段，成功返回 `True`。 |
| | `has_section(name)` | 檢查一個區段是否存在。 |
| | `options(section)` | 取得指定區段中所有選項（設定鍵）名稱的列表。 |
| | `has_option(section, option)` | 檢查指定區段中的選項是否存在。 |
| | `remove_option(section, option)` | 移除指定區段中的一個選項，成功返回 `True`。 |
| **II. 存取與類型轉換** | `get(section, option, fallback=None)` | 取得選項的原始**字串**值，可設定備用值。 |
| | `getint(section, option, fallback=None)` | 取得選項的值並轉換為**整數**。 |
| | `getfloat(section, option, fallback=None)` | 取得選項的值並轉換為**浮點數**。 |
| | `getboolean(section, option, fallback=None)` | 取得選項的值並轉換為**布林值** (`True`/`False`)。 |
| | `set(section, option, value)` | 設定或修改指定區段中選項的值。 |
| **III. 配置屬性** | `defaults()` | 包含 **DEFAULT** 區段值的字典。 |
| | `default_section` | 預設區段的名稱，通常為 `'DEFAULT'`。 |
| | `delimiters` | 接受的鍵/值分隔符列表（預設為 `['=', ':']`）。 |
