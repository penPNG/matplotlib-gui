import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,      # Oh my god I'm not the first person to think of this horrible thing.
    NavigationToolbar2Tk    # IT'S BUILT IN
)
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
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
        self.data = Text(self, width= 40, height=20, wrap="word", font="Consolas 15")    # Creates a textbox that has word wrapping and uses the Consolas font at size 15
        vs = ttk.Scrollbar(self, orient='vertical', command=self.data.yview) # Instantiates a scrollbar for the textbox
        self.data.config(yscrollcommand=vs.set)      # Modifies the vertical scroll command for the textbox to use the scrollbar
        vs.grid(column=2, row =0, sticky='ns', columnspan=1)  # Puts the scrollbar on the screen, right next to the textbox, stuck to the top and bottom of the row
        self.data.grid(column=0, row=0, columnspan=2)              # Puts the textbox on the screen, it's rather tall

        opn = ttk.Button(self, text="Open", command=self.test) # The open button, opens a file of indeterminable type
        opn.focus()                # Auto focuses the button for easy enter use
        opn.grid(column=0, row=1, sticky='sw', pady=5, padx=5)  # Puts the button directly below the textbox for 'convenience'

        test = ttk.Button(self, text="test", command=self.test)
        test.grid(column=1, row=1, sticky='sw', pady=5, padx=5)

        fig = Figure(figsize=(5,4), dpi=100)    # The figure. Oh if only I knew how matplotlib worked
        ax = fig.add_subplot()              # Some more
        ax.bar(self.words, self.numbers)    # matplotlib
        ax.set_title('words and numbers')   # bullshit
        ax.set_ylabel('numbers')

        canvas = FigureCanvasTkAgg(fig, self)           # Create the canvas
        canvas.get_tk_widget().grid(column=3, row=0, padx=15)    # Put the canvas in frame
        canvas.draw()                                   # Draw the canvas

        navFrame = Frame(self)  # A frame specifically for the navbar. I pray to god that it works
        navFrame.grid(column=3, row=0, sticky='sw')
        navbar = NavigationToolbar2Tk(canvas, navFrame) # it works


        
    def openFile(self):
        fe = [("Text Document","*.txt"),("Excel files","*.xlsx")]   # Right now, it doesn't open excel file properly. I'll have to do some pandas magic for that.
        file = filedialog.askopenfilename(filetypes=fe) # Starts a dialog for opening a file
        self.f=open(file)   # Opens the file in python
        self.updateData()

    def test(self):
        self.dh.test(self.data.get(1.0, 'end-1c'))
        print(self.data.get(1.0, 'end-1c'))

    def updateData(self):
        self.data.delete(1.0, END)
        self.data.insert(1.0, self.f.read())