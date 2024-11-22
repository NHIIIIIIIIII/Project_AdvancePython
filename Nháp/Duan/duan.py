import tkinter as tk

def click_button(operation):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                result = "Cannot divide by zero"
            else:
                result = num1 / num2
        else:
            result = "Invalid operation"
            label_result.config(text="Result: " + str(result))

    except ValueError:
        label_result.config(text="Invalid input")

root = tk.Tk()
root.title("Simple Calculator")

label_num1 = tk.Label(root, text="Enter first number:")
label_num1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label_num2 = tk.Label(root, text="Enter second number:")
label_num2.pack()

entry2 = tk.Entry(root)
entry2.pack()

button_add = tk.Button(root, text="+", command=lambda: click_button('+'))
button_subtract = tk.Button(root, text="-", command=lambda: click_button('-'))
button_multiply = tk.Button(root, text="*", command=lambda: click_button('*'))
button_divide = tk.Button(root, text="/", command=lambda: click_button('/'))

button_add.pack(side=tk.LEFT)
button_subtract.pack(side=tk.LEFT)
button_multiply.pack(side=tk.LEFT)
button_divide.pack(side=tk.LEFT)

label_result = tk.Label(root, text="")
label_result.pack()

root.mainloop()
