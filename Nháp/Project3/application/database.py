import psycopg2
from psycopg2 import sql

def get_db_connection(db_name, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connection established successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_data(conn, table_name):
    try:
        cur = conn.cursor()
        query = sql.SQL("SELECT masach, tensach, mota, ngayxuatban FROM {}").format(sql.Identifier(table_name))
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def insert_data(conn, table_name, data):
    try:
        cur = conn.cursor()
        query = sql.SQL("INSERT INTO {} (masach, tensach, mota, ngayxuatban) VALUES (%s, %s, %s, %s)").format(sql.Identifier(table_name))
        cur.execute(query, data)
        conn.commit()
        cur.close()
        print("Data inserted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting data: {e}")

def delete_data(conn, table_name, book_id):
    try:
        cur = conn.cursor()
        query = sql.SQL("DELETE FROM {} WHERE masach = %s").format(sql.Identifier(table_name))
        cur.execute(query, (book_id,))
        conn.commit()
        cur.close()
        print("Data deleted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error deleting data: {e}")

def update_data(conn, table_name, data):
    try:
        cur = conn.cursor()
        query = sql.SQL("UPDATE {} SET masach=%s, tensach=%s, mota=%s, ngayxuatban=%s WHERE masach=%s").format(sql.Identifier(table_name))
        cur.execute(query, data)
        conn.commit()
        cur.close()
        print("Data updated successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating data: {e}")
