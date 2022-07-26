import re
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,      # Oh my god I'm not the first person to think of this horrible thing.
    NavigationToolbar2Tk    # IT'S BUILT IN
)
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd
from data.dataHandling import DataHandling

# This is the best frame to ever frame anything ever.
class TheFrame(Frame):
    def __init__(self, container):
        super().__init__(container)
        
        matplotlib.use('TkAgg') # Apparently, I'm not the first person to think of this monstrosity.
        self.d = {
            'this': 25.1,
            'is': 13.5,
            'temp': 15.6,
            'data': 20
        }
        self.words = self.d.keys()
        self.numbers = self.d.values()

        self.dh = DataHandling()

        self.initUI()
    
    def initUI(self):
        self.textBox = Text(self, width= 40, height=20, wrap="word", font="Consolas 15")    # Creates a textbox that has word wrapping and uses the Consolas font at size 15
        vs = ttk.Scrollbar(self, orient='vertical', command=self.textBox.yview) # Instantiates a scrollbar for the textbox
        self.textBox.config(yscrollcommand=vs.set)      # Modifies the vertical scroll command for the textbox to use the scrollbar
        vs.grid(column=4, row =0, sticky='ns')  # Puts the scrollbar on the screen, right next to the textbox, stuck to the top and bottom of the row
        self.textBox.grid(column=0, row=0, columnspan=4)              # Puts the textbox on the screen, it's rather tall

        opn = ttk.Button(self, text="Open", command=self.openFile) # The open button, opens a file of indeterminable type
        opn.focus()                # Auto focuses the button for easy enter use
        opn.grid(column=0, row=1, sticky='sw', pady=5, padx=5)  # Puts the button directly below the textbox for 'convenience'

        # Ideally, it should plot the chart on the first try, but should that not happen, this button is for reorganizing data
        # in the textbox. It allows you to modify data opened from file without writing to file.
        # Also, should I want to write to file, the only type i'll ever do is text, despite how easy exporting to excel might be.
        rload = ttk.Button(self, text="Reload", command=self.createDict)
        rload.grid(column=1, row=1, sticky='sw', pady=5, padx=5)
        
        self.radios = IntVar()
        self.radios.set(1) # Set default radio button to Tabs
        spaces = ttk.Radiobutton(self, variable=self.radios, text="Spaces", value=0, command=self.changeToSpaces)  # Separate by spaces
        tabs = ttk.Radiobutton(self, variable=self.radios, text="Tabs", value=1, command=self.changeToTabs)       # Separate by tabs
        spaces.grid(column=2, row=1, sticky='w', padx=5, pady=5)
        tabs.grid(column=3, row=1, sticky='w', padx=5, pady=5)
        

        fig = Figure(figsize=(5,4), dpi=100)    # The figure. Oh if only I knew how matplotlib worked
        ax = fig.add_subplot()              # Some more
        ax.bar(self.words, self.numbers)    # matplotlib
        ax.set_title('words and numbers')   # bullshit
        ax.set_ylabel('numbers')

        canvas = FigureCanvasTkAgg(fig, self)           # Create the canvas
        canvas.get_tk_widget().grid(column=7, row=0, padx=15)    # Put the canvas in frame
        canvas.draw()                                   # Draw the canvas

        navFrame = Frame(self)  # A frame specifically for the navbar. I pray to god that it works
        navFrame.grid(column=7, row=0, sticky='sw')
        navbar = NavigationToolbar2Tk(canvas, navFrame) # it works


    def changeToSpaces(self):
        d = self.textBox.get(1.0, END)
        d = d.replace('\t', ' ')
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, d)

    def changeToTabs(self):
        d = self.textBox.get(1.0, END)
        d = d.replace(' ', '\t')
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, d)

        
    def openFile(self):
        fe = [("Text Document","*.txt"),("Excel files","*.xlsx")]   # Right now, it doesn't open excel file properly. I'll have to do some pandas magic for that.
        file = filedialog.askopenfilename(filetypes=fe) # Starts a dialog for opening a file
        if file.endswith(".txt"):
            self.f=open(file)   # Opens the file in python
            self.updateData()   # Updates the textbox
            self.createDict()   
            self.data = self.dh.organizeInSet(self.dataDict)    # Put text data in dataframe
            self.fixData(1)
            self.fixTime()
        elif file.endswith(".xlsx"):
            self.handleExcel(file)
            self.fixTime()
            
    def fixData(self, istxt):
        # So basically, I have to do some addition and data handling and im not gonna use the class i made specifically for that reason.
        # I need to get the titles of the columns because they COULD be diffferent/nonstandard
        colname = self.data.columns
        if istxt:
            self.data[colname[0]] = pd.to_numeric(self.data[colname[0]])
            self.data[colname[1]] = pd.to_datetime(self.data[colname[1]])
            self.data[colname[1]] = self.data[colname[1]].dt.strftime("%H:%M")
            print(self.data)
            

    def createDict(self):
        self.textBox.delete('end-1c')  # Remove the last character, usually is a newline character.
        self.dataDict = self.dh.createDict(self.textBox.get(1.0, 'end-1c'), self.radios.get()) # Create a dictionary with the data
        print(self.textBox.get(1.0, 'end-1c'))

    def updateData(self):   # Update text in textbox with file information
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, self.f.read())
        
    # I'm just gonna write one function for both excel and text files for this. It should just work over all. Fingers crossed
    def fixTime(self):
        column = self.data.columns
        wrongTime = self.data[column[1]].astype(str)
        count = 0
        for row in wrongTime:
            wrongTime[count] = "00:"+wrongTime[count]
            count+=1
        self.data[column[1]] = pd.to_datetime(wrongTime).dt.strftime("%M:%S")
        print(self.data[column[1]])
        
    # Super cool comment describing data frames
        #   min     cause
    #0  1   1:30    db
    #1  2   2:03    db
    #2  3   1:47    db

    # There is a discrepancy in the index and the count. For our purposes we can ignore the index, or label it as #-1 should we need to use it

    def handleExcel(self, f):
        self.data = pd.read_excel(f)  # I think I can just have one data variable across all formats.
        colname=self.data.columns     # Grab a list of the column names, so capitalization/names are whatever
        self.data[colname[1]] = self.data[colname[1]].astype(str)   # Change to a string
        self.data[colname[1]] = pd.to_datetime(self.data[colname[1]]).dt.strftime("%H:%M")  # And then change back into datetime
        # Literally shouldn't have to do this, but pandas is dumb.
        print(self.data)
        #ef[colname[1]] = ef[colname[1]].dt.strftime("%M:%S")
        self.data.groupby(colname[0]).plot.pie(y=colname[0])
        if self.radios.get():   # If we are using tabs
            self.textBox.delete(1.0, END)  # Clear textbox
            count = 0
            for name in colname:
                self.textBox.insert(END, name) # Insert column name into textbox
                count += 1
                if count < 3:
                    self.textBox.insert(END, '\t') # If it's not the last name, put a tab after
            for index, row in self.data.iterrows():
                self.textBox.insert(END, '\n') # newline for formatting
                count = 0
                for col in row:
                    self.textBox.insert(END, str(col)) # Start inserting data into the textbox
                    count += 1
                    if count < 3:
                        self.textBox.insert(END, '\t') # If it's not the last item in row, put a tab after

            
        print(self.data)