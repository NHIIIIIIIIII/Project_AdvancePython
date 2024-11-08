import tkinter as tk
from tkinter import Menu, ttk, messagebox, filedialog
import pandas as pd
import database  # Import file database.py chứa các hàm liên quan đến cơ sở dữ liệu

class BookDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('icon.ico')
        self.root.title("Book Database App")
        
        # Các trường thông tin cơ sở dữ liệu
        self.db_name = tk.StringVar(value='dbbooks')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='books')
        self.conn = None  # Khởi tạo biến kết nối

        # Hiển thị khung kết nối
        self.connection_frame()
    
    def connection_frame(self):
        self.connection_frame = tk.Frame(self.root)
        self.connection_frame.grid(pady=10)

        tk.Label(self.connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Host:").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.host).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Port:").grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.port).grid(row=1, column=3, padx=5, pady=5)

        connect_button = tk.Button(self.connection_frame, text="Connect", command=self.connect_to_database)
        connect_button.grid(row=2, column=3, columnspan=2, pady=10)

    def connect_to_database(self):
        self.conn = database.connect_db(self.db_name.get(), self.user.get(), self.password.get(), self.host.get(), self.port.get())
        if self.conn:
            self.connection_frame.grid_forget()
            self.show_db_interface()

    def show_db_interface(self):
        # Tạo frame mới cho giao diện chính
        self.db_interface_frame = tk.Frame(self.root)
        self.db_interface_frame.grid(pady=10)

        # Frame để nhập dữ liệu
        insert_frame = ttk.LabelFrame(self.db_interface_frame, text="Insert Data")
        insert_frame.grid(pady=10, column=0)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()
        self.column3 = tk.StringVar()
        self.column4 = tk.StringVar()

        tk.Label(insert_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=1, column=0, padx=5, pady=5)

        tk.Label(insert_frame, text="Book Name:").grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Description:").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column3).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(insert_frame, text="Publish Date:").grid(row=0, column=3, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column4).grid(row=1, column=3, padx=5, pady=5)

        # Frame cho các nút chức năng
        button_frame = ttk.LabelFrame(self.db_interface_frame, text="Actions")
        button_frame.grid(padx=5, pady=10, column=2, row=0, rowspan=3)
        tk.Button(button_frame, text="Load Data", command=self.load_data).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Insert Data", command=self.insert_data).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="Delete Data", command=self.delete_data).grid(row=2, column=0, columnspan=2, pady=10)

        # Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(self.db_interface_frame, columns=("masach", "tensach", "mota", "ngayxuatban"), show="headings")
        self.tree.heading("masach", text="Book ID")
        self.tree.heading("tensach", text="Book Name")
        self.tree.heading("mota", text="Description")
        self.tree.heading("ngayxuatban", text="Publish Date")
        self.tree.grid(pady=10, columnspan=6)

        # Load dữ liệu sau khi kết nối thành công
        self.load_data()

    def load_data(self):
        if self.conn:
            rows = database.get_data(self.conn, self.table_name.get())
            self.display_data(rows)

    def display_data(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def insert_data(self):
        data = (self.column1.get(), self.column2.get(), self.column3.get(), self.column4.get())
        database.insert_data(self.conn, self.table_name.get(), data)
        self.load_data()

    def delete_data(self):
        book_id = self.column1.get()
        database.delete_data(self.conn, self.table_name.get(), book_id)
        self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookDatabaseApp(root)
    root.mainloop()
