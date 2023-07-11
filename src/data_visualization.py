import tkinter as tk
from tkinter import PhotoImage, ttk, font

COLOR = '#%02x%02x%02x' % (174, 239, 206)

class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        heading = tk.Label(self,text="My Project",font= font.Font(size=25), padx=20, justify="left")
        heading.pack(anchor=tk.W)

        InfoEntry(self)
        VisualizationEntry(self)
        SummaryEntry(self)

class InfoEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
		
        self.pack(expand = True, fill = 'both', padx = 20, pady = 20)

    def create_widgets(self):
        # Create the first frame
        infoFrame = tk.Frame(self, bg='red')
        infoFrame.grid(row=0, column=0, pady=10, sticky='nsew')

        # Set the grid weights to control the resizing behavior
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=6)
        self.grid_columnconfigure(1, weight=4)

        # Create the first sub-frame
        sub_frame1 = tk.Frame(infoFrame, bg='green')
        sub_frame1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Create the second sub-frame
        sub_frame2 = tk.Frame(infoFrame, bg='green')
        sub_frame2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        infoFrame.grid_rowconfigure(0, weight=1)
        infoFrame.grid_columnconfigure(0, weight=5)
        infoFrame.grid_columnconfigure(1, weight=5)
        # Add widgets to the frames
        
        height = tk.Label(sub_frame1, text=f"Height", justify='left')
        height.pack()
        weight = tk.Label(sub_frame1, text=f"Weight", justify='left')
        weight.pack()
        bmi = tk.Label(sub_frame1, text=f"BMI", justify='left')
        bmi.pack()

        date = tk.Label(sub_frame2, text=f"Date", justify='right')
        date.pack()
        time = tk.Label(sub_frame2, text=f"Time", justify='right')
        time.pack()
        creater = tk.Label(sub_frame2, text=f"Creater", justify='right')
        creater.pack()

        # Create the second frame
        optionFrame = tk.Frame(self, bg='blue')
        optionFrame.grid(row=0, column=1, pady=10, sticky='nsew')

        backButton = tk.Button(optionFrame, text ="Go Back", bg= COLOR, bd=0, width=20, padx=20, )
        backButton.pack( pady=10)
        saveButton = tk.Button(optionFrame, text ="Save as PDF",bg= COLOR, bd=0,width=20,padx=20 )
        saveButton.pack( pady=10)

class VisualizationEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack( expand=True, fill="both", padx = 20, pady = 20)
        self.create_canvas()

    def create_canvas(self):
        # Create a canvas widget
        canvas = tk.Canvas(self, height="600")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar widget
        scrollbar = ttk.Scrollbar(self, orient = 'vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")


        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))

        # Create a frame inside the canvas to hold the content
        frame = tk.Frame(canvas)
        frame.grid(sticky="ew")


        # Add widgets to the frame
        GraphEntry(frame)
        GraphEntry(frame)

        # Place the frame inside the canvas
        canvas.create_window((0, 0), window=frame, anchor="nw")

class GraphEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand = True, fill = 'both')
        self.create_widget()

    def create_widget(self):
        # Create three frames
        heading_frame = tk.Frame(self, bg="red",padx=50, pady=10, height=50,width=1500)
        graph_frame = tk.Frame(self, bg="green", padx=50, pady=10, height=200,width=1500 )
        information_frame = tk.Frame(self, bg="blue", padx=10, pady=10, height=200,width=1500)

        # Configure grid layout manager
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Place frames using grid layout
        heading_frame.grid(row=0, column=0, sticky="ew", pady=(10,0))
        graph_frame.grid(row=1, column=0, sticky="ew", )
        information_frame.grid(row=2, column=0, sticky="ew",  pady=(0,10))

        self.create_graphs(graph_frame)


    def create_graphs(self, parentFrame):
        # Create the first frame

        BarGraph = tk.Frame(parentFrame, bg='red', height=100)
        BarGraph.grid(row=0, column=0, pady=10, sticky='nsew')

        # Set the grid weights to control the resizing behavior
        parentFrame.grid_rowconfigure(0, weight=1)
        parentFrame.grid_columnconfigure(0, weight=7)
        parentFrame.grid_columnconfigure(1, weight=3)

        # Create the second frame
        PieChart = tk.Frame(parentFrame, bg='blue', height=100)
        PieChart.grid(row=0, column=1, pady=10, sticky='nsew')

class SummaryEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand = True, fill = 'both')
        self.create_table()
    def create_table(self):
        table = ttk.Treeview(self, columns = (1,2,3,4,5,6), show = 'headings')
        table.pack()

        heading = ["Movement", 'Evaluation Time', 'Minimum No', 'Minimum Frequency', 'Maximum No.', 'Minimum Frequency']
        movement = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        evaluation_Time = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']
        min_number = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        min_frequency = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        max_number = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']
        max_frequency = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        table_data = [movement,evaluation_Time, min_number, min_frequency, max_number, max_frequency]

        COLOR = '#%02x%02x%02x' % (174, 239, 206)
        table.tag_configure('oddrow', background='white')
        table.tag_configure('evenrow', background=COLOR)
        table.tag_configure("heading", font=('TkDefaultFont', 10, 'bold'))


        # Add the header row to the Treeview
        table.insert("", "end", text="", values=heading, tags="heading")    

        for i, row in enumerate(table_data):
            # Determine the tag for the row
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'

            # Insert the row into the Treeview
            table.insert('', 'end', values=row, tags=(tag,))
            

        scrollbar_table = ttk.Scrollbar(self, orient = 'vertical', command = table.yview)
        table.configure(yscrollcommand = scrollbar_table.set)
        scrollbar_table.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')