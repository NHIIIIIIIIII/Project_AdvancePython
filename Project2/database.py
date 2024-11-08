import psycopg2
from psycopg2 import sql
from tkinter import messagebox

# Hàm kết nối đến cơ sở dữ liệu
def connect_db(db_name, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        messagebox.showinfo("Success", "Connected to the database successfully!")
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to the database: {e}")
        return None

# Hàm lấy toàn bộ dữ liệu từ bảng
def get_data(conn, table_name):
    try:
        cur = conn.cursor()
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {e}")
        return []

# Hàm chèn dữ liệu vào bảng
def insert_data(conn, table_name, data):
    try:
        cur = conn.cursor()
        query = sql.SQL("INSERT INTO {} (masach, tensach, mota, ngayxuatban) VALUES (%s, %s, %s, %s)").format(
            sql.Identifier(table_name)
        )
        cur.execute(query, data)
        conn.commit()
        cur.close()
        messagebox.showinfo("Success", "Data inserted successfully!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error inserting data: {e}")

# Hàm xóa dữ liệu theo ID
def delete_data(conn, table_name, book_id):
    try:
        cur = conn.cursor()
        query = sql.SQL("DELETE FROM {} WHERE masach = %s").format(sql.Identifier(table_name))
        cur.execute(query, (book_id,))
        conn.commit()
        cur.close()
        messagebox.showinfo("Success", "Data deleted successfully!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Error deleting data: {e}")
