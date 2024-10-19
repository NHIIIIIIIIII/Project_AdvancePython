import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
import pandas as pd
class TableApp():
    def __init__(self,root):
        # Khởi tạo lớp cha (DBconnection)
        self.root = root
        self.root.iconbitmap('icon.ico')
        self.root.title("Kết nối database")
       
        #  - Frame cho menu
        self.menu_bar = Menu(self.root)
         # File menu
        file_menu = Menu(self.menu_bar,tearoff=0)
        self.menu_bar.add_cascade(label="File" , menu=file_menu)
        file_menu.add_command(label="Xuất",command=self.export_to_excel)
        # Help_menux
        help_menu = Menu(self.menu_bar, tearoff=0)  
        self.menu_bar.add_cascade(label="Help", menu=help_menu)  
        help_menu.add_command(label="About",command=self.msg_box_info)
        help_menu.add_command(label="Exit",command= self.quit_app)
        self.root.config(menu=self.menu_bar)
        
        self.root.title("Quản lý sinh viên")
       
        # # Create menu and add menu items
        # file_menu = Menu(self.menu_bar , tearoff=0) # create File menu  , mất cái - - - 
        # file_menu.add_command(label="New") # add File menu item
        # file_menu.add_separator()

        # file_menu.add_command(label="Exit")
        # self.menu_bar.add_cascade(label="File", menu=file_menu) # add File menu  to menu bar and give it a label

        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')
        
        width = 900
        height = 700
        self.root.geometry(f"{height}x{width}")

        screen_width = self.root.winfo_screenwidth()  # Lấy chiều rộng màn hình
        screen_height = self.root.winfo_screenheight()  # Lấy chiều cao màn hình
        # Tính toán tọa độ để đặt cửa sổ ở giữa
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        # Đặt kích thước và vị trí của cửa sổ
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Giao diện connect db
        self.widgets_connect() 

    def widgets_connect(self):


        self.connection_frame = tk.Frame(self.root)
        self.connection_frame.pack(pady=10)

        tk.Label(self.connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self.connection_frame, text="Connect", command= self.connect_to_manage).grid(row=5, columnspan=2, pady=10)

    # def widgets_login(self):
    #     self.login_frame = tk.Frame(self.root)
    #     self.login_frame.pack()
    #     username = tk.StringVar()
    #     tk.Label(self.login_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
    #     tk.Entry(self.login_frame, textvariable=username).grid(row=1, column=1, padx=5, pady=5)

    #     password = tk.StringVar()
    #     tk.Label(self.login_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
    #     tk.Entry(self.login_frame, textvariable=password, show="*").grid(row=2, column=1, padx=5, pady=5)
    #     tk.Button(self.connection_frame, text="Connect", command= self.trans_to_login).grid(row=5, columnspan=2, pady=10)

    
    def widgets_manage(self):
        
        # Khung chứa bảng
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10)

        # Tạo bảng Treeview
        self.data_table = ttk.Treeview(self.table_frame, columns=("MSSV", "Tên Sinh Viên"), show="headings", height=10)
        self.data_table.heading("MSSV", text="MSSV")
        self.data_table.heading("Tên Sinh Viên", text="Tên Sinh Viên")
        self.data_table.column("MSSV", width=100)
        self.data_table.column("Tên Sinh Viên", width=200)
        self.data_table.pack()
        # Thêm sự kiện để lấy thông tin hàng được chọn
        # <ButtonRelease-1>: Đây là sự kiện khi người dùng thả nút chuột trái ra (sau khi nhấn vào nó).
        self.data_table.bind("<ButtonRelease-1>", self.on_tree_select)
        self.load_data()
        # Khung chứa các ô nhập liệu
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        # Nhãn và ô nhập MSSV
        ttk.Label(form_frame, text="MSSV : ").grid(row=0, column=0, padx=5, pady=5)
        self.mssv = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.mssv).grid(row=0, column=1, padx=5, pady=5)

        # Nhãn và ô nhập Họ Tên
        ttk.Label(form_frame, text="Họ Tên : ").grid(row=1, column=0, padx=5, pady=5)
        self.hoten = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.hoten).grid(row=1, column=1, padx=5, pady=5)
        
        # Nút để thêm hàng mới
        add_button = ttk.Button(form_frame, text="Thêm hàng mới", command=self.on_add_button_click)
        add_button.grid(column=0,row=2,padx=5, pady=10)
        
        # Nút để load data
        load_button = ttk.Button(form_frame, text="Load data", command=self.load_data)
        load_button.grid(column=1,row=2,padx=5, pady=10)
        # Nút để xóa data đang chọn
        delete_button = ttk.Button(form_frame, text="Xóa hàng đang chọn", command=self.delete_selected_row)
        delete_button.grid(column=2,row=2,padx=5, pady=10)
        
        # Nút để xóa data trong ô
        delete_input_button = ttk.Button(form_frame, text="Xóa dữ liệu trong ô mssv", command= self.delete_data_input)
        delete_input_button.grid(column=3,row=2,padx=5, pady=10)
        
        # Nút clear input
        clear_button = ttk.Button(form_frame, text="Xóa nội dung trong ô", command=self.clear_inputs)
        clear_button.grid(column=4,row=2,padx=5, pady=10)

        
    def on_tree_select(self, event):
        """Xử lý khi người dùng chọn hàng trong Treeview"""
        selected_items = self.data_table.selection()
        if selected_items:
            item = selected_items[0]  # Lấy hàng đầu tiên được chọn
            values = self.data_table.item(item, 'values')  # Lấy dữ liệu của hàng đã chọn
            mssv = values[0]  # MSSV nằm ở cột đầu tiên
            hoten = values[1]  # Họ tên nằm ở cột thứ hai
            # Cập nhật giá trị vào các ô nhập liệu
            self.mssv.set(mssv)
            self.hoten.set(hoten)
            
    def on_add_button_click(self):
        """Thêm sinh viên mới vào cơ sở dữ liệu và bảng Treeview"""
        mssv = self.mssv.get().strip()
        hoten = self.hoten.get().strip()

        if self.validate_input(mssv, hoten):
            if self.insert_data() :
                self.add_table(mssv, hoten)
                self.clear_inputs()

    def validate_input(self, mssv, hoten):
        """Kiểm tra đầu vào không được để trống."""
        if not mssv or not hoten:
            messagebox.showwarning("Lỗi nhập liệu", "MSSV và Họ Tên không được để trống.")
            return False
        return True

    def add_table(self, mssv, hoten):
        """Thêm hàng mới vào bảng Treeview."""
        new_row = (mssv, hoten)
        self.data_table.insert("", tk.END, values=new_row)

    def clear_inputs(self):
        """Xóa các ô nhập liệu sau khi thêm dữ liệu thành công."""
        self.mssv.set("")
        self.hoten.set("")
    
    def connect_db(self):
        """Kết nối tới cơ sở dữ liệu PostgreSQL"""
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
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")
            return False
        
    def load_data(self):
        """Tải dữ liệu từ cơ sở dữ liệu và hiển thị trong bảng Treeview"""
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            # Dấu * là giải nén tuple thành các phần tử riêng lẻ
            self.data_table.delete(*self.data_table.get_children())  # Xóa toàn bộ dữ liệu hiện tại
            for row in rows:
                # các hàng được chèn không có quan hệ cha-con
                self.data_table.insert("", tk.END, values=row)  # Thêm từng hàng dữ liệu
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        """Chèn dữ liệu sinh viên vào cơ sở dữ liệu"""
        try:
            insert_query = sql.SQL("INSERT INTO {} (mssv, hoten) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.mssv.get(), self.hoten.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            return True
        except Exception as e: 
            messagebox.showerror("Error", f"Error inserting data: {e}")
            return False

    def delete_selected_row(self):
        """Xóa hàng đang được chọn trong Treeview"""
        try:
            selected_items = self.data_table.selection()  # Lấy tất cả các hàng đang được chọn
            if not selected_items:
                messagebox.showwarning("Lỗi", "Vui lòng chọn hàng để xóa.")
                return

            for item in selected_items:
                values = self.data_table.item(item, 'values')  # Lấy dữ liệu của hàng đã chọn
                mssv = values[0]  # Giả sử MSSV nằm ở cột đầu tiên
                # Xóa dữ liệu trong cơ sở dữ liệu
                self.delete_data(mssv)

                # Xóa hàng từ Treeview (chỉ xóa nếu nó còn tồn tại)
                if item in self.data_table.get_children():
                    self.data_table.delete(item)
                else:
                    messagebox.showwarning("Lỗi", f"Item {item} không tồn tại trong bảng.")
            self.clear_inputs()
            messagebox.showinfo("Thành công", "Đã xóa hàng thành công.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting selected row: {e}")

    def delete_data_input(self):
        try:
            
            self.delete_data(self.mssv.get())
            self.load_data()
            self.clear_inputs()
            messagebox.showinfo("Success","Đã xóa thành công")
        except Exception as e:
            messagebox.showerror("Error",f"{e}")
    
    
    def delete_data(self, mssv):
        """Xóa dữ liệu sinh viên khỏi cơ sở dữ liệu theo MSSV"""
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (mssv,))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data from database: {e}")

    def connect_to_manage(self):
        check = self.connect_db()
        if check:
            self.connection_frame.pack_forget()
            self.widgets_manage()
        else :
            pass
             
    
    
    def check_login(self):
        """Chèn dữ liệu sinh viên vào cơ sở dữ liệu"""
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            for i in rows :
                print(i)
            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def msg_box_info(self):
        messagebox.showinfo("About","This is a GUI made by Hieu Tran \n Today is 10/13/2024")
        # messagebox.askquestion("Tỏ tình","Làm ny mình nhé")
    
    def quit_app(self):
        self.root.destroy()  # Hủy cửa sổ Tkinter và thoát ứng dụng
        
    def export_to_excel(self):
        try :
            rows = []
            # Lấy tất cả các ID của hàng trong Treeview
            for item in self.data_table.get_children():
                # Lấy giá trị của từng hàng
                row_data = self.data_table.item(item)['values']
                # Thêm giá trị đó vào danh sách rows
                rows.append(row_data)
            # Kiểu giá trị tuple
            # Tạo DataFrame
            df = pd.DataFrame(rows, columns=["MSSV", "Họ Tên"])

            # Xuất ra file Excel
            # Thêm thì mất cột chỉ mục stt [index=False]
            df.to_excel("sinhvien.xlsx")
            messagebox.showinfo("Xuất file", "Dữ liệu đã được xuất ra file Excel thành công!")
        except Exception as e :
            messagebox.showwarning("Warning",f"Bạn cần connect databse để sử dụng \n {e}")
if __name__ == "__main__":
    root = tk.Tk()
    TableApp(root)
    root.mainloop()