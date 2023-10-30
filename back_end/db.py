import sqlite3

DATABASE = 'database.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS data;')
    c.execute('''CREATE TABLE data (
        id INTEGER PRIMARY KEY,
        encrypted TEXT
    );''')

    conn.commit()
    conn.close()


# 增
def insert_data(encrypted_data):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO data (encrypted) VALUES (?)", (encrypted_data,))
    conn.commit()
    conn.close()


# 删
def delete_data(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM data WHERE id = ?", (id,))
    rows_affected = conn.total_changes  # 获取受影响的行数
    conn.commit()
    conn.close()
    return rows_affected


# 查
def fetch_data(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT encrypted FROM data WHERE id = ?", (id,))
    encrypted_data = c.fetchone()
    conn.close()
    return encrypted_data[0] if encrypted_data else None


# 查最新
def get_latest_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT encrypted FROM data ORDER BY ROWID DESC LIMIT 1")
    data = c.fetchone()
    conn.close()
    return data[0] if data else None


# 查所有
def fetch_all_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, encrypted FROM data")  # 获取 id 和 encrypted
    encrypted_data = c.fetchall()
    conn.close()
    return [{"id": data[0], "encrypted": data[1]} for data in encrypted_data] if encrypted_data else []


# 改
def update_data(id, new_encrypted_data):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE data SET encrypted = ? WHERE id = ?", (new_encrypted_data, id))
    conn.commit()
    conn.close()


# 统计总数
def get_data_count():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM data")
    count = c.fetchone()[0]
    conn.close()
    return count


# 模拟SQL注入攻击，不安全的查询
def unsafe_query(search_term):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(f"SELECT encrypted FROM data WHERE encrypted LIKE '%{search_term}%'")  # 非参数化查询
    encrypted_data = c.fetchall()
    conn.close()
    return encrypted_data
