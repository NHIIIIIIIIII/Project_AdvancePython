import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox

# Tạo cửa sổ GUI
win = tk.Tk()
win.title("Chuyển đổi đơn vị")

win.iconbitmap('Project1/icon.ico')
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text = "Độ dài")
tabControl.add(tab2, text = "Cân nặng")

tabControl.pack(expand=1, fill="both")
# Hộp chọn loại quy đổi
conversion_type_label = ttk.Label(tab1, text="Chọn đơn vị quy đổi:")
conversion_type_label.grid(column=0, row=0)

conversion_type = tk.StringVar()
conversion_combobox = ttk.Combobox(tab1, width=10, state="readonly", textvariable=conversion_type)   #Hộp chọn loại quy đổi
conversion_combobox['values'] = ("km","m","cm","mm")
conversion_combobox.grid(column=2, row=1)
conversion_combobox.current(0)  # Mặc định chọn loại quy đổi đầu tiên

conversion_type2 = tk.StringVar()
conversion_combobox2 = ttk.Combobox(tab1, width=10, state="readonly", textvariable=conversion_type2)   #Hộp chọn loại quy đổi
conversion_combobox2['values'] = ("km","m","cm","mm")
conversion_combobox2.grid(column=2, row=2)
conversion_combobox2.current(0)

# Nhãn và ô nhập cho giá trị đầu vào
input_label = ttk.Label(tab1, text="Nhập giá trị:")
input_label.grid(column=0, row=1)

input_value = tk.DoubleVar()  # Biến lưu trữ giá trị nhập vào và làm việc với các giá trị số thực và cần chúng được cập nhật tự động trên giao diện người dùng
entry_box = ttk.Entry(tab1, textvariable=input_value, width=10)
entry_box.grid(column=1, row=1)

# Ô hiển thị kết quả
result_label = ttk.Label(tab1, text="Kết quả:")
result_label.grid(column=0, row=2)

result_value = tk.DoubleVar()       #lưu trữ và làm việc với các giá trị số thực và cần chúng được cập nhật tự động trên giao diện người dùng.
result_entry = ttk.Entry(tab1, textvariable=result_value, state="disable", width=10)
result_entry.grid(column=1, row=2)

# Hàm thực hiện quy đổi
def convert_units():
    try:
        value = input_value.get()
        conversion = conversion_combobox.get()
        conversion2 = conversion_combobox2.get()
        
        if conversion == "km":
            if conversion2 == "km":
                result = value
            elif conversion2 == "m":
                result = value * 1000
            elif conversion2 == "cm":
                result = value * 100000
            elif conversion2 == "mm":
                result = value * 1000000
        elif conversion == "m":
            if conversion2 == "km":
                result = value / 1000
            elif conversion2 == "m":
                result = value
            elif conversion2 == "cm":
                result = value * 100
            elif conversion2 == "mm":
                result = value * 1000
        elif conversion == "cm":
            if conversion2 == "km":
                result = value / 100000
            elif conversion2 == "m":
                result = value / 100
            elif conversion2 == "cm":
                result = value
            elif conversion2 == "mm":
                result = value * 10
        elif conversion == "mm":
            if conversion2 == "km":
                result = value / 1000000
            elif conversion2 == "m":
                result = value / 1000
            elif conversion2 == "cm":
                result = value / 10
            elif conversion2 == "mm":
                result = value

        result_value.set(format(result, '.10f').rstrip('0').rstrip('.'))

    except tk.TclError:
        mbox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ")

# Nút thực hiện quy đổi
convert_button = ttk.Button(tab1, text="Quy đổi", command=convert_units)
convert_button.grid(column=1, row=4, columnspan=2)

# CÂN NẶNG
# Hộp chọn loại quy đổi
tab2_label = ttk.Label(tab2, text="Chọn đơn vị quy đổi:")
tab2_label.grid(column=0, row=0)

# Hộp chọn đơn vị quy đổi đầu vào
tab2_conversion_type = tk.StringVar()
tab2_conversion_combobox = ttk.Combobox(tab2, width=10, state="readonly", textvariable=tab2_conversion_type)   # Hộp chọn loại quy đổi
tab2_conversion_combobox['values'] = ("kg", "g", "mg")
tab2_conversion_combobox.grid(column=2, row=1)
tab2_conversion_combobox.current(0)

# Hộp chọn đơn vị quy đổi đầu ra
tab2_conversion_type2 = tk.StringVar()
tab2_conversion_combobox2 = ttk.Combobox(tab2, width=10, state="readonly", textvariable=tab2_conversion_type2)   # Hộp chọn loại quy đổi
tab2_conversion_combobox2['values'] = ("kg", "g", "mg")
tab2_conversion_combobox2.grid(column=2, row=2)
tab2_conversion_combobox2.current(0)

# Nhãn và ô nhập cho giá trị đầu vào
tab2_input_label = ttk.Label(tab2, text="Nhập giá trị:")
tab2_input_label.grid(column=0, row=1)

tab2_input_value = tk.DoubleVar()  # Biến lưu trữ giá trị nhập vào
tab2_entry_box = ttk.Entry(tab2, textvariable=tab2_input_value, width=10)
tab2_entry_box.grid(column=1, row=1)

# Ô hiển thị kết quả
tab2_result_label = ttk.Label(tab2, text="Kết quả:")
tab2_result_label.grid(column=0, row=2)

tab2_result_value = tk.StringVar()  # Biến lưu trữ kết quả
tab2_result_entry = ttk.Entry(tab2, textvariable=tab2_result_value, state="readonly", width=10)
tab2_result_entry.grid(column=1, row=2)

# Hàm thực hiện quy đổi
def convert_units():
    try:
        tab2_value = tab2_input_value.get()
        tab2_conversion = tab2_conversion_combobox.get()
        tab2_conversion2 = tab2_conversion_combobox2.get()
        
        # Điều kiện quy đổi cân nặng (kg, g, mg)
        if tab2_conversion == "kg":
            if tab2_conversion2 == "kg":
                result = tab2_value
            elif tab2_conversion2 == "g":
                result = tab2_value * 1000
            elif tab2_conversion2 == "mg":
                result = tab2_value * 1000000
        elif tab2_conversion == "g":
            if tab2_conversion2 == "kg":
                result = tab2_value / 1000
            elif tab2_conversion2 == "g":
                result = tab2_value
            elif tab2_conversion2 == "mg":
                result = tab2_value * 1000
        elif tab2_conversion == "mg":
            if tab2_conversion2 == "kg":
                result = tab2_value / 1000000
            elif tab2_conversion2 == "g":
                result = tab2_value / 1000
            elif tab2_conversion2 == "mg":
                result = tab2_value
        
        # Hiển thị kết quả sau khi quy đổi
        tab2_result_value.set(format(result, '.10f').rstrip('0').rstrip('.'))
    
    except tk.TclError:
        mbox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ")

# Nút thực hiện quy đổi
tab2_convert_button = ttk.Button(tab2, text="Quy đổi", command=convert_units)
tab2_convert_button.grid(column=1, row=4, columnspan=2)

win.mainloop()

