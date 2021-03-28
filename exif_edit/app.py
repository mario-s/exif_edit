"""
GUI of the application.
"""

import sys
import logging
import tkinter as tk
import tkinter.filedialog as filedialog

from tkinter import ttk
from idlelib import tooltip as tp
from tksheet import Sheet

from exif_edit.mediator import Mediator


class App(tk.Tk):

    """This class contains the GUI. It uses a spreadsheet to display Exif Tags."""

    def __init__(self):
        super().__init__()
        self.img_display = None

        self.title("Exif Edit")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.protocol("WM_DELETE_WINDOW", self.__quit)

        self.frame = tk.Frame(self)
        self.frame.grid(row = 1, column = 0, sticky = "nswe")
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)

        self.sheet = Sheet(self.frame,
            headers = ["Key", "Value"],
            column_width = 250,
            page_up_down_select_row = True,
            total_columns=2,
            empty_horizontal=5, empty_vertical=5,
            height=500, width = 550)
        self.mediator = Mediator(self.sheet)
        
        self.__add_menubar()
        self.__add_toolbar()
        self.__add_sheet()
        self.__add_table_commands()

    def __add_menubar(self): 
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Open", accelerator="Cmd+O", command=self.__open)
        filemenu.add_command(label="Save", accelerator="Cmd+S", command=self.__save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", accelerator="Cmd+W", command=self.__quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        #add key bindings according to accelerators
        self.bind('<Command-o>', self.__open)
        self.bind('<Command-s>', self.__save)
        self.bind('<Command-w>', self.__quit)

    def __add_toolbar(self):
        self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        self.toolbar.grid(row = 0, column = 0, sticky = "nswe")

        btn_open = self.__create_toolbar_button("folder.png", 
            "open file " + self.__acc("O"), 
            self.__open)
        btn_open.pack(side=tk.LEFT, padx=2, pady=5)
        btn_save = self.__create_toolbar_button("save-file.png", 
            "save file " + self.__acc("S"), 
            self.__save)
        btn_save.pack(side=tk.LEFT, padx=2, pady=5)
        btn_exit = self.__create_toolbar_button("exit.png", 
            "exit "+ self.__acc("W"), 
            self.__quit)
        btn_exit.pack(side=tk.LEFT, padx=2, pady=5)

        sep = ttk.Separator(self.toolbar, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, padx=2, pady=5, fill='y')
        btn_loc = self.__create_toolbar_button("world.png", 
            "show location",
            self.__open_location)
        btn_loc.pack(side=tk.LEFT, padx=2, pady=5)

    def __create_toolbar_button(self, icon_name, tooltip, cmd):
        icon = self.mediator.read_icon(icon_name)
        btn = tk.Button(self.toolbar, image=icon, relief=tk.FLAT, command=cmd)
        btn.image = icon
        Tooltip(btn, text=tooltip)
        return btn

    @classmethod
    def __acc(cls, key):
        return "(" + (u"\u2318") + f"{key})"

    def __add_sheet(self):
        self.sheet.grid(row = 0, column = 0, padx=5, pady=5, sticky = "nswe")
        self.sheet.enable_bindings(("single_select", 
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

        self.sheet.extra_bindings([("cell_select", self.cell_select),
                                ("begin_edit_cell", self.begin_edit_cell),
                                ("end_edit_cell", self.end_edit_cell),
                                ("row_select", self.row_select),
                                ("deselect", self.deselect),
                                ("drag_select_rows", self.drag_select_rows)
                                ])
        
    def __add_table_commands(self):
        left_cmd_frame = tk.Frame(self.frame, borderwidth=2)
        left_cmd_frame.grid(row = 1, column = 0, sticky = "nswe")

        btn_add = tk.Button(left_cmd_frame, text="+", command=self.mediator.add_row)
        btn_add.pack(padx=5, pady=3, side=tk.LEFT)
        Tooltip(btn_add, "add a row")

        self.btn_rm = tk.Button(left_cmd_frame, text="-", command=self.mediator.remove_row, 
            state=tk.DISABLED)
        self.btn_rm.pack(padx=5, pady=3, side=tk.LEFT)
        Tooltip(self.btn_rm, "remove selected rows")

    def load_image(self, img_path):
        """
        This method loads the image and the exif data into the application.
        """
        logging.info("loading image: %s", img_path)

        self.mediator.append_exif(img_path)

        #destroy a possible previous instance to avoid a stack of images
        if not self.img_display is None:
            self.img_display.destroy()

        img = self.mediator.read_image(img_path)
        self.img_display = tk.Label(self.frame, image=img)
        self.img_display.image = img
        self.img_display.grid(row = 0, column = 1, padx=5, pady=5, sticky = "w")

        #ensure that window has focus again
        self.focus_set()

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
        self.eval('tk::PlaceWindow . center')
        self.mainloop()
    
    def __open(self, event = None):
        name = filedialog.askopenfilename()
        self.load_image(name)

    def __save(self, event = None):
        self.mediator.save_exif()

    def __open_location(self, event = None):
        self.mediator.open_location()

    @classmethod 
    def __quit(cls, event = None):
        sys.exit(0)

class Tooltip(tp.Hovertip):

    def __init__(self, anchor_widget, text, hover_delay = 2000):
        super().__init__(anchor_widget, text, hover_delay=hover_delay)

    def showcontents(self):
        label = tk.Label(self.tipwindow, text=self.text, 
                    justify=tk.LEFT, relief=tk.SOLID,
                    foreground="#000000", background="#ffffe0", borderwidth=1)
        label.pack()