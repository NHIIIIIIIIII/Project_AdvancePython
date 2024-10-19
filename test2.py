import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox, filedialog
import psycopg2
from psycopg2 import sql
import pandas as pd

class Test:
    def __init__(self,win):
        self.win = win
        self.win.title("Test")
        self.connection_frame()


    def validation(self):
        if  self.number.get() > 10 :
            return True
        else : 
            return False
       

    def change(self):
        if self.validation() :
            self.connection_frame.pack_forget()
            self.connected_frame()
        else:
            messagebox.showerror("Error", "Số lớn hơn 10 tk ngu")
        
 
    
    def connection_frame(self):

        # Frame connect 
        self.connection_frame = tk.Frame(self.win)
        self.connection_frame.pack(pady=10)
        tk.Label(self.connection_frame, text="Connect Frame").grid(column=0,row=0)
        change_button = tk.Button(self.connection_frame,text="Ấn để đổi",command=self.change)
        change_button.grid(column=0 , row=1)
        self.number = tk.IntVar()
        tk.Entry(self.connection_frame,textvariable=self.number,width=12).grid(column=0,row=2)
        # TODO yêu cầu nhập số >10 mới cho qua
    
    def connected_frame(self):
        # Frame test
        testframe = tk.Frame(self.win)
        testframe.pack(pady=10)
        tk.Label(testframe, text="Test Frame").grid(column=0,row=3)
        tk.Button(testframe, text="Destroy Frame",command=self.exit_widgets).grid(column=0,row=0)

    def exit_widgets(self):
        self.win.destroy()
        
        
        
        
        
        
        
        
        
if __name__ == "__main__":

    win = tk.Tk()
    Test(win)
    win.mainloop()