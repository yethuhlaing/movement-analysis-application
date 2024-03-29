import tkinter as tk
import time
import threading
from tkinter import Canvas, ttk, font
from PIL import Image, ImageTk
from database import *
from configparser import ConfigParser
from tkinter import messagebox 
from data import *
from utils import *
from data_visualization import DataVisualization

COLOR = '#%02x%02x%02x' % (174, 239, 206)
class LandingPage(ttk.Frame):
    def __init__(self, parent):
        self.root = parent
        tk.Frame.__init__(self, self.root, bg="white")
        self.pack(expand=True, fill="both")
        
        #font Style
        self.button_font = font.Font(family="Bookman Old Style", size=10)
        self.text_font = font.Font(family="Bookman Old Style", size=10)
        self.heading_font = font.Font(family="Bookman Old Style", size=20, weight="bold")

        
        # Database Path
        config = ConfigParser()
        config.read('config.ini')
        self.db_path = config.get('Database', 'database_path')
        self.create_widgets()
        
    def create_widgets(self):
        # Background image
        # Using the configure even image is resized to the window size
        # Implementing a delay in the resizing possibly makes it smoother
        bg_image = Image.open("../assets/landing_page_bg.png")
        bg_image = bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas = Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        canvas.grid(row=0, column=0, columnspan=3)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        def resizer(event):
            global bg1, resized_bg, new_bg # Needed for garbage collector
            bg1 = Image.open("../assets/landing_page_bg.png")
            resized_bg = bg1.resize((event.width, event.height),Image.Resampling.LANCZOS)
            new_bg = ImageTk.PhotoImage(resized_bg)
            canvas.create_image(0, 0, image=new_bg, anchor="nw")
        self.bind('<Configure>', resizer)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Overlay canvas for the left column
        overlay_canvas = Canvas(self, width=self.winfo_screenwidth() // 2, height=self.winfo_screenheight(), bg="white", highlightthickness=0)
        overlay_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Heading Label
        welcome_label = tk.Label(overlay_canvas, text="Welcome to Movement Analysis!", font=self.heading_font, padx=20,  bg="white")
        welcome_label.pack(pady=50)

        # Create a frame for recent projects
        recent_projects_frame = tk.Frame(overlay_canvas, background = "white")
        recent_projects_frame.pack()
        recent_projects_label = tk.Label(recent_projects_frame, text="Recent Projects", font=self.text_font, bg="white")
        recent_projects_label.pack(pady = 5)
        self.createRecentProject(recent_projects_frame)

        # Create three frames
        frame1 = tk.Frame(overlay_canvas, bg="white")
        frame2 = tk.Frame(overlay_canvas, bg="white")
        frame3 = tk.Frame(overlay_canvas, bg="white")

        # Pack the frames on the right side
        frame1.pack(fill="x", pady= (90,0))
        frame2.pack(fill="x")
        frame3.pack(fill="x")


        # Project Name
        self.project_name_entry = ttk.Entry(frame1, width=30)
        self.project_name_entry.pack( side="right")
        project_name_label = tk.Label(frame1, text="Project Name:", font=self.text_font, bg="white", padx=10, pady=5)
        project_name_label.pack(side="right")


        # Project Creator
        self.project_creator_entry = ttk.Entry(frame2, width=30)
        self.project_creator_entry.pack( side="right")
        project_creator_label = tk.Label(frame2, text="Project Creator:", font=self.text_font, bg="white", padx=10, pady=5)
        project_creator_label.pack(side="right")

    
        # Start Button
        start_button = tk.Button(frame3, text="Create", bg=COLOR, bd=0,width=20,padx=10 , font=self.button_font, command=self.start_app)
        start_button.pack(side="right", pady=20)

    def createRecentProject(self, parent):
        selected = tk.StringVar()
        self.combobox = ttk.Combobox(parent, width=75, textvariable=selected, values=["All", *self.comboboxOptions()], font=self.text_font)
        self.combobox.bind("<<ComboboxSelected>>", self.on_combo_select)
        self.combobox.pack( padx=(20,0), pady=10)

        self.treeView = ttk.Treeview(parent, columns=(1,2,3,4,5), height=13, show="headings", )
        self.treeView.column(1, anchor="center", stretch="no", width=80)
        self.treeView.column(2, anchor="center", stretch="no", width=140)
        self.treeView.column(3, anchor="center", stretch="no", width=140)
        self.treeView.column(4, anchor="center", stretch="no", width=140)
        self.treeView.column(5, anchor="center", stretch="no", width=140)

        self.treeView.heading(1, text="No.")
        self.treeView.heading(2, text="Project")
        self.treeView.heading(3, text="Scenario")
        self.treeView.heading(4, text="Student")
        self.treeView.heading(5, text="Created")
        self.displayData()
        self.treeView.pack(padx= (20,0))


        deleteButton = tk.Button(parent, text ="Delete",bg= COLOR, bd=0,width=20,padx=10 , font=self.button_font, command=self.deleteHistory)
        deleteButton.pack( pady=10, anchor="e", padx=5, side="right")
        openButton = tk.Button(parent, text ="Open",bg= COLOR, bd=0,width=20,padx=10 , font=self.button_font, command=self.openHistory )
        openButton.pack( pady=10, anchor="e", padx=5, side="right")
        
    def comboboxOptions(self):
        project_list = selectAllProject(self.db_path)
        return [ project[0] for project in project_list]
         
    def displayData(self):
        histories = retreiveHistory(self.db_path)
        for index, history in enumerate(histories, start=0):
            student_id = history[0] 
            project = history[1]
            scenario = history[2]  
            student = history[3]
            createdDate = history[4]
            self.treeView.insert('',index, value=(student_id, project, scenario, student, createdDate))
        self.treeView.bind("<ButtonRelease-1>", self.on_click)
        self.treeView.bind("<Double-1>", self.on_double_click)
        
    def on_combo_select(self, event):
        for item in self.treeView.get_children():
            self.treeView.delete(item)
        selectedProject = self.combobox.get()
        self.selectedHistory = None
        if selectedProject == "All":
            self.displayData()
        else:
            selectedHistories = retreiveSelectedHistory(self.db_path, selectedProject)
            for index, selectedHistory in enumerate(selectedHistories, start=0):
                self.treeView.insert('',index, values=selectedHistory)
            self.treeView.bind("<ButtonRelease-1>", self.on_click)

    def on_click(self, event):
        history = self.treeView.identify_row(event.y)
        if history:
            history_id = history
            self.selectedHistory = self.treeView.item(history_id, "values")
            # print("Clicked item values:", self.selectedHistory) 

    def deleteHistory(self):
        result = messagebox.askyesno("Confirmation", f"Do you want to delete?")
        if result:
            if self.selectedHistory != None:
                student_id = self.selectedHistory[0]
                deleteHistory(self.db_path, student_id)
                for item in self.treeView.get_children():
                    self.treeView.delete(item)    
                self.displayData()
                self.combobox['values'] = ["All", *self.comboboxOptions() ]  
            else:       
                messagebox.showerror("Error", "Please select the project before you delete!")
                
    def openHistory(self):
        result = messagebox.askyesno("Confirmation", f"Do you want to open this?")
        if result:
            if self.selectedHistory != None:
                student_id = self.selectedHistory[0]
                reference_df, student_df , status_df = retrieveSelectedDataframeList(self.db_path, student_id)        
                userData = retrieveSelectedUserList(self.db_path, student_id)
                setUserData(userData)
                setReference_df(reference_df)
                setStudent_df(student_df)
                setStatus_df(status_df)
                self.LoadingAndExecutePage()
            else:       
                messagebox.showerror("Error", "Please select the project before you open!")

    def on_double_click(self, event):
        self.on_click(event)
        self.openHistory()

    def show_loading_animation(self):

        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Loading...")

        # Create a Canvas widget to cover the entire window with a black overlay
        self.loading_canvas = tk.Canvas(self.loading_window, bg="white", highlightthickness=0, highlightbackground="white")
        self.loading_canvas.pack(fill=tk.BOTH, expand=True)
        # Center the loading window on the screen
        self.loading_window.update_idletasks()  # Update to get actual window size
        screen_width = self.loading_window.winfo_screenwidth()
        screen_height = self.loading_window.winfo_screenheight()
        window_width = self.loading_window.winfo_width()
        window_height = self.loading_window.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.loading_window.geometry(f"+{x}+{y}")

        self.loading_frame = tk.Frame(self.loading_canvas, width=x, height=y, background="white")
        self.loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.loading_label = tk.Label(self.loading_frame, text="Please wait for a while", bg="white")
        self.loading_label.pack()


        self.loading_canvas.update_idletasks()
        self.loading_canvas.config(scrollregion=self.loading_canvas.bbox("all"))
        self.loading_window.transient(self.root)
        self.loading_window.grab_set()
   
    def simulate_page_loading(self):
        # Switch to Data Visualization Page
        time.sleep(4)
        self.master.show_visualize_data()
        self.pack_forget()

        # Create a label with a loading message or an animated gif
        self.loading_label.destroy()
        self.loading_window.title("Finished Loading!")
        loadingContents = getLoadingContents()
        for loadingContent in loadingContents:
            loading_label = tk.Label(self.loading_frame, text=f"{loadingContent}", background="white",font=("Bookman Old Style", 8))
            loading_label.pack(anchor=tk.CENTER, pady=3)
            time.sleep(0.25)
        # Close the loading window when loading is done
        self.root.after(1000, self.close_loading_window)

    def close_loading_window(self):

        # Close the loading window
        if self.loading_window:
            self.loading_window.destroy()
            self.loading_window = None

    def LoadingAndExecutePage(self):
        self.show_loading_animation()
        # Start a new thread to execute the page loading process
        loading_thread = threading.Thread(target=self.simulate_page_loading)
        loading_thread.start()





    def start_app(self):
        project_name = self.project_name_entry.get()
        project_creator = self.project_creator_entry.get()
        # Switch to the project creation page and pass the project name
        self.master.show_project_creation(project_name,project_creator)

  