import sys
import logging
import tkinter as tk
import tkinter.filedialog as filedialog

from tksheet import Sheet

from exif_edit.mediator import Mediator


class App:

    """This class contains the GUI. It uses a spreadsheet to display Exif Tags."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Exif Edit")
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.protocol("WM_DELETE_WINDOW", self.__quit)

        self.frame = tk.Frame(self.root)
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        
        self.__add_sheet()
        self.__add_menubar()
        self.__add_commands()

    def __add_sheet(self):
        sheet = Sheet(self.frame, page_up_down_select_row = True,
            headers = ["Key", "Value"],
            height = 500, width = 550)
        sheet.grid(row = 0, column = 0)
        sheet.enable_bindings(("single_select", 
                                "drag_select",   
                                "row_select",
                                "row_height_resize",
                                "double_click_row_resize",
                                "rc_select",
                                "rc_insert_column",
                                "rc_delete_column",
                                "rc_insert_row",
                                "rc_delete_row",
                                "copy",
                                "cut",
                                "paste",
                                "delete",
                                "undo",
                                "edit_cell"))

        sheet.extra_bindings([("cell_select", self.cell_select),
                                ("begin_edit_cell", self.begin_edit_cell),
                                ("end_edit_cell", self.end_edit_cell),
                                ("row_select", self.row_select),
                                ("deselect", self.deselect),
                                ("drag_select_rows", self.drag_select_rows)
                                ])
        self.mediator = Mediator(sheet)
        self.sheet = sheet

    def __add_menubar(self): 
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Open", accelerator="Cmd+O", command=self.__open)
        filemenu.add_command(label="Save", accelerator="Cmd+S", command=self.__save)
        filemenu.add_command(label="Exit", accelerator="Cmd+W", command=self.__quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        #add key bindings according to accelerators
        self.root.bind('<Command-o>', self.__open)
        self.root.bind('<Command-s>', self.__save)
        self.root.bind('<Command-w>', self.__quit)
        
    def __add_commands(self):
        left_cmd_frame = tk.Frame(self.frame, borderwidth=2)
        left_cmd_frame.grid(row = 1, column = 0, sticky = "nswe")
        btn_add = tk.Button(left_cmd_frame, text="+", command=self.mediator.add_row)
        btn_add.pack(padx=5, pady=5, side=tk.LEFT)
        self.btn_rm = tk.Button(left_cmd_frame, text="-", command=self.mediator.remove_row, 
            state=tk.DISABLED)
        self.btn_rm.pack(padx=5, pady=5, side=tk.LEFT)

        right_cmd_frame = tk.Frame(self.frame, borderwidth=2)
        right_cmd_frame.grid(row = 1, column = 1, sticky = "nswe")
        btn_exit = tk.Button(right_cmd_frame, text="exit", command=self.__quit)
        btn_exit.pack(padx=5, pady=5, side=tk.RIGHT)
        btn_save = tk.Button(right_cmd_frame, text="save", command=self.__save)
        btn_save.pack(padx=5, pady=5, side=tk.RIGHT)

    def load_image(self, img_path):
        logging.info("loading image: %s", img_path)

        self.mediator.append_exif(img_path)

        image = self.mediator.read_image(img_path)
        label = tk.Label(self.frame, image=image)
        label.image = image
        label.grid(row = 0, column = 1, padx=5, pady=5, sticky = "nswe")

        self.root.focus_set()

    def single_select(self, event):
        print(event)

    def drag_select_rows(self, event):
        self.__change_button_state(event)
    
    def begin_edit_cell(self, event):
        self.mediator.keep_origin((event[0], event[1])) 

    def end_edit_cell(self, event):
        self.mediator.restore_origin((event[0], event[1]))

    def mouse_motion(self, event):
        region = self.sheet.identify_region(event)
        row = self.sheet.identify_row(event, allow_end = False)
        column = self.sheet.identify_column(event, allow_end = False)
        print (region, row, column)

    def deselect(self, event):
        self.__change_button_state(event)
        
    def cell_select(self, event):
        self.__change_button_state(event)

    def row_select(self, event):
        self.__change_button_state(event)

    def __change_button_state(self, event):
        print(event)
        self.btn_rm.config(state=self.mediator.get_remove_button_state(event))

    def start(self):
        #https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()
    
    def __open(self, event = None):
        name = filedialog.askopenfilename()
        self.load_image(name)

    def __save(self, event = None):
        self.mediator.save_exif()

    @classmethod 
    def __quit(cls, event = None):
        sys.exit(0)
