from tkinter import *
from tkinter import ttk
from tkinter import filedialog


# Old dumb code that I'm not gonna use lol
class ControlFrame(Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.initUI()
    
    def initUI(self):
        open = ttk.Button(self, text="Open", command=self.openFile) # The open button, opens a file of indeterminable type
        open.focus()                # Auto focuses the button for easy enter use
        open.grid(column=0, row=0)  # Puts the button directly below the textbox for 'convenience'

        
    def openFile(self):
        file = filedialog.askopenfilename() # Starts a dialog for opening a file
        self.f=open(file)   # Opens the file in python
        #self.f.close()      # Closes the file because I haven't done anything with it yet