from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class ControlFrame(Frame):
    
    def __init__(self, root, padding, relief):
        super().__init__()
        
        self.root = root
        self.initUI()
    
    def initUI(self):
        self.grid()
        
        ttk.Button(self, text="Quit", command=self.openFile).grid(column=1, row=0)
        
    def openFile(self):
        file = filedialog.askopenfilename()
        f=open(file)
        print(f.read())

