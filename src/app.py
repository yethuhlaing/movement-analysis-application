import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter.messagebox import showinfo

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Movement Analysis')

        #setting tkinter window size
        width= self.winfo_screenwidth()
        height= self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))

        # logo
        p1 = PhotoImage(file = 'lab-logo.png')
        self.iconphoto(False, p1)
        

    def button_clicked(self):
        showinfo(title='Information', message='Hello, Tkinter!')

if __name__ == "__main__":
    app = App()
    app.mainloop()
