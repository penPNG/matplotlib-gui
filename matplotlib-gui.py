import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from controlFrame import ControlFrame

root = Tk()
data = ttk.Frame(root, padding=10, relief="sunken")
data.grid()
ttk.Label(data, text="Hello World!").grid(column=0,row=1)
#filename = filedialog.askopenfilename()


def main():
    root = Tk()
    cf = ControlFrame(root, padding=10, relief="raised")
    root.mainloop()

if __name__ == "__main__":
    main()