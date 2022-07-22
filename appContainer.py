from tkinter import Tk
from controlFrame import ControlFrame
from theFrame import TheFrame

class AppContainer(Tk):
    def __init__(self):
        super().__init__()
        self.title('matplotlib-gui')    # Title of the window/container

        self.createFrames()
        

    def createFrames(self):
        # I think I'm just gonna put the controls in the same frame as the textbox, and then somehow put the data I open into matplotlib.
        # You know what? I'm just gonna put it all in one frame. For shits and giggles. Fuck object oriented programming.

        #control_frame = ControlFrame(self)  # There will be the open and save buttons, open opening a file, and save saving whatever matplotlib shows
        #control_frame.grid(column=0, row=1) # Here is where that frame belongs

        # This comes after the control_frame so that I can pass it into the textbox_frame to access the file data and display in the textbox
        textbox_frame = TheFrame(self)  # The textbox has it's own frame incase you're a psycho and want to type the data yourself
        textbox_frame.grid(column=0, row=0) # Here is where that frame belongs