import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox, filedialog
import psycopg2
from psycopg2 import sql
import pandas as pd

class BookDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('icon.ico')
        self.root.title("Book Database App")

        # - Frame cho menu
        self.menu_bar = Menu(self.root)
        # File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export to Excel", command=self.export_to_excel)

        self.root.config(menu=self.menu_bar)

        # Database connection fields
        self.db_name = tk.StringVar(value='dbbooks')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='books')

        # Create the GUI elements
        self.create_connection()
        self.create_query()
    
    
        
    def create_connection(self):
        # Connection section
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)
        # connection_frame.grid(padx=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=1, column=3, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=2, column=3, columnspan=2, pady=10)

    def create_query(self):
        # Query section
        query_frame = tk.Frame(self.root)
        query_frame.pack(pady=10)

        tk.Label(query_frame, text="Table Name:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=3, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Load Data", command=self.load_data).grid(row=3, column=3, columnspan=2, pady=10)

        # Insert section
        insert_frame = tk.Frame(self.root)
        insert_frame.pack(pady=10)

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

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(insert_frame, text="Delete Data", command=self.delete_data).grid(row=2, column=2, columnspan=2, pady=10)

        # Treeview to display data
        self.tree = ttk.Treeview(self.root, columns=("masach", "tensach", "mota", "ngayxuatban"), show="headings")
        self.tree.heading("masach", text="Book ID")
        self.tree.heading("tensach", text="Book Name")
        self.tree.heading("mota", text="Description")
        self.tree.heading("ngayxuatban", text="Publish Date")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Clear the Treeview before inserting new data
            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in rows:
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def export_to_excel(self):
        try:
            rows = []
            # Lấy tất cả các ID của hàng trong Treeview
            for item in self.tree.get_children():
                # Lấy giá trị của từng hàng
                row_data = self.tree.item(item)['values']
                # Thêm giá trị đó vào danh sách rows
                rows.append(row_data)

            # Kiểm tra xem Treeview có dữ liệu hay không
            if not rows:
                messagebox.showwarning("Warning", "Không có dữ liệu để xuất!")
                return

            # Lấy tên cột từ Treeview
            col_names = [self.tree.heading(col)['text'] for col in self.tree["columns"]]

            # Tạo DataFrame
            export_excel = pd.DataFrame(rows, columns=col_names)

            # Sử dụng hộp thoại để lưu file
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                # Xuất ra file Excel
                export_excel.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Dữ liệu đã được xuất ra file Excel tại {file_path}")
            else:
                messagebox.showwarning("Warning", "Bạn chưa chọn vị trí để lưu file.")

        except Exception as e:
            messagebox.showerror("Error", f"Đã xảy ra lỗi khi xuất dữ liệu ra file Excel: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (masach, tensach, mota, ngayxuatban) VALUES (%s, %s, %s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get(), self.column3.get(), self.column4.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def delete_data(self):
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE masach = %s").format(sql.Identifier(self.table_name.get()))
            data_to_delete = (self.column1.get(),)
            self.cur.execute(delete_query, data_to_delete)
            self.conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookDatabaseApp(root)
    root.mainloop()
