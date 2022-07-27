import re
import matplotlib as plt
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
        
        plt.use('TkAgg') # Apparently, I'm not the first person to think of this monstrosity.
        self.example = pd.DataFrame({
            'data': [pd.Timedelta(hours=0,minutes=1,seconds=30),pd.Timedelta(hours=0,minutes=0, seconds=47), 
                     pd.Timedelta(hours=0,minutes=18, seconds=17)]
        })
        #self.words = self.example.keys()
        #self.numbers = self.example.values()

        self.dh = DataHandling()

        self.initUI()
    
    def initUI(self):
        self.textBox = Text(self, width= 40, height=20, wrap="word", font="Consolas 15")    # Creates a textbox that has word wrapping and uses the Consolas font at size 15
        vs = ttk.Scrollbar(self, orient='vertical', command=self.textBox.yview) # Instantiates a scrollbar for the textbox
        self.textBox.config(yscrollcommand=vs.set)      # Modifies the vertical scroll command for the textbox to use the scrollbar
        vs.grid(column=4, row =0, sticky='ns')  # Puts the scrollbar on the screen, right next to the textbox, stuck to the top and bottom of the row
        self.textBox.grid(column=0, row=0, columnspan=4)    # Puts the textbox on the screen, it's rather tall

        opn = ttk.Button(self, text="Open", command=self.openFile) # The open button, opens a file of indeterminable type
        opn.focus()                # Auto focuses the button for easy enter use
        opn.grid(column=0, row=1, sticky='sw', pady=5, padx=5)  # Puts the button directly below the textbox for 'convenience'

        # Ideally, it should plot the chart on the first try, but should that not happen, this button is for reorganizing data
        # in the textbox. It allows you to modify data opened from file without writing to file.
        # Also, should I want to write to file, the only type i'll ever do is text, despite how easy exporting to excel might be.
        rload = ttk.Button(self, text="Reload", command=self.reloadData)
        rload.grid(column=1, row=1, sticky='sw', pady=5, padx=5)
        
        self.radios = IntVar()
        self.radios.set(1) # Set default radio button to Tabs
        spaces = ttk.Radiobutton(self, variable=self.radios, text="Spaces", value=0, command=self.changeToSpaces)  # Separate by spaces
        tabs = ttk.Radiobutton(self, variable=self.radios, text="Tabs", value=1, command=self.changeToTabs)       # Separate by tabs
        spaces.grid(column=2, row=1, sticky='w', padx=5, pady=5)
        tabs.grid(column=3, row=1, sticky='w', padx=5, pady=5)
        
        self.example['data'] = self.timeToSec(self.example['data'])
        #self.fig = Figure(figsize=(5,4), dpi=100)    # The figure. Oh if only I knew how matplotlib worked
        self.fig = self.example.plot.pie(title="Example", y='data', figsize=(5,4)).get_figure()
        #ax = fig.add_subplot()              # Some more
        #fig, ax = plt.subplots()
        #ax.pie(self.numbers, labels=self.words)    # matplotlib
        #ax.set_title('words and numbers')   # bullshit
        #ax.set_ylabel('numbers')
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)           # Create the canvas
        self.canvas.get_tk_widget().grid(column=7, row=0, padx=15)    # Put the canvas in frame
        self.canvas.draw()                                   # Draw the canvas

        navFrame = Frame(self)  # A frame specifically for the navbar. I pray to god that it works
        navFrame.grid(column=7, row=0, sticky='sw')
        navbar = NavigationToolbar2Tk(self.canvas, navFrame) # it works


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
            self.fixTextData()
            self.fixTime()
        elif file.endswith(".xlsx"):
            self.handleExcel(file)
            self.fixTime()
            
    def fixTextData(self):
        # So basically, I have to do some addition and data handling and im not gonna use the class i made specifically for that reason.
        # I need to get the titles of the columns because they COULD be diffferent/nonstandard
        colname = self.data.columns
        self.data[colname[0]] = pd.to_numeric(self.data[colname[0]])
        self.data[colname[1]] = pd.to_datetime(self.data[colname[1]])
        print(self.data)    # Debugging
            
    def reloadData(self):   # Recrates the dictionary with what's in the textox
        self.createDict()
        self.data = self.dh.organizeInSet(self.dataDict)
        self.fixTextData()
        self.total = self.dh.addTime(self.data) # Just gonna sneak this in here while the formatting is juuuuuust right
        self.fixTime()
        self.timeToSec(self.data['min'])

    def timeToSec(self, d):
        time = d.astype(str)
        seconds = []
        for t in time:
            if len(t) <= 5:
                mn = int(t[:2])*60
                sc = int(t[3:])
                sc += mn
                seconds.append(sc)
            elif len(t) >= 7:
                if 'days' in t:
                    t = t[7:]
                hr = int(t[:2])*60
                mn =(int(t[3:5])*60)+hr
                sc = int(t[6:])
                sc += mn
                seconds.append(sc)
        return(seconds)

    def createDict(self):
        self.textBox.delete('end-1c')  # Remove the last character, usually is a newline character.
        self.dataDict = self.dh.createDict(self.textBox.get(1.0, 'end-1c'), self.radios.get()) # Create a dictionary with the data
        print(self.textBox.get(1.0, 'end-1c'))  # Debugging

    def updateData(self):   # Update text in textbox with file information
        self.textBox.delete(1.0, END)
        self.textBox.insert(1.0, self.f.read())
        
    # I'm just gonna write one function for both excel and text files for this. It should just work over all. Fingers crossed
    def fixTime(self):
        colname = self.data.columns  # Can never be too careful
        #self.data[colname[1]] = self.data[colname[1]].dt.strftime("%H:%M") # Funny enough, this is done when adding.
        wrongTime = self.data[colname[1]].astype(str)    # I could probably do this without creating a new series, but whatever
        count = 0
        for row in wrongTime:
            wrongTime[count] = "00:"+wrongTime[count]   # This is a little easier with the new variable
            count+=1
        self.data[colname[1]] = pd.to_datetime(wrongTime).dt.strftime("%M:%S")   # pandas is DUMB
        print(self.data[colname[1]]) # Debugging
        
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
        print(self.data)    # Debugging
        #ef[colname[1]] = ef[colname[1]].dt.strftime("%M:%S")
        #self.data.groupby(colname[0]).plot.pie(y=colname[0])   # Not there yet
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

            
        print(self.data)    # Debugging