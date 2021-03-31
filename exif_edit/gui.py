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

from PIL import ImageFilter
from PIL import ImageTk as itk

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
        self.__add_bindings()

    def __add_menubar(self): 
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Open", accelerator="Cmd+O", command=self.__open)
        filemenu.add_command(label="Save", accelerator="Cmd+S", command=self.__save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", accelerator="Cmd+W", command=self.__quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def __add_toolbar(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        toolbar.grid(row = 0, column = 0, sticky = "nswe")

        btn_open = ToolbarButton(toolbar, self.__icon("folder.png"), 
            "open file " + self.__acc("O"), 
            self.__open)
        btn_open.pack(side=tk.LEFT, padx=2, pady=5)

        btn_save = ToolbarButton(toolbar, self.__icon("save-file.png"), 
            "save file " + self.__acc("S"), 
            self.__save)
        btn_save.pack(side=tk.LEFT, padx=2, pady=5)

        btn_exit = ToolbarButton(toolbar, self.__icon("exit.png"), 
            "exit "+ self.__acc("W"), 
            self.__quit)
        btn_exit.pack(side=tk.LEFT, padx=2, pady=5)

        sep = ttk.Separator(toolbar, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, padx=2, pady=5, fill='y')

        self.btn_loc = ToolbarButton(toolbar, self.__icon("world.png"), 
            "show location " + self.__acc("L"),
            self.__open_location)
        self.btn_loc.pack(side=tk.LEFT, padx=2, pady=5)

    def __icon(self, icon_name):
        return self.mediator.read_icon(icon_name)

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

    def __add_bindings(self):
        #add key bindings according to accelerators
        self.bind('<Command-o>', self.__open)
        self.bind('<Command-s>', self.__save)
        self.bind('<Command-w>', self.__quit)
        self.bind('<Command-l>', self.__open_location)

    def load_image(self, img_path):
        """
        This method loads the image and the exif data into the application.
        """
        logging.info("loading image: %s", img_path)

        self.mediator.append_exif(img_path)

        #destroy a possible previous instance to avoid a stack of images
        if not self.img_display is None:
            self.img_display.destroy()

        img = itk.PhotoImage(self.mediator.read_image(img_path))
        self.img_display = tk.Label(self.frame, image=img)
        self.img_display.image = img
        self.img_display.grid(row = 0, column = 1, padx=5, pady=5, sticky = "w")

        self.__update_location_button()

        #ensure that window has focus again
        self.focus_set()

    def __update_location_button(self):
        with_loc = self.mediator.has_location()
        if with_loc:
            self.btn_loc.enable()
        else:
            self.btn_loc.disable()

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

class ToolbarButton(tk.Button):
    """
    Button for the toolbar.
    """
    def __init__(self, anchor, icon, tooltip, cmd):
        self.icon = icon.convert("RGBA")
        self.image = itk.PhotoImage(self.icon)
        super().__init__(anchor, image=self.image, relief=tk.FLAT, command=cmd)
        Tooltip(self, text=tooltip)

    def disable(self):
        self.config(state=tk.DISABLED)
        icon = self.icon.copy()
        im = icon.filter(ImageFilter.EMBOSS)
        self.image = itk.PhotoImage(im)
        self.config(image=self.image)

    def enable(self):
        self.config(state=tk.NORMAL)
        icon = self.icon.copy()
        self.image = itk.PhotoImage(icon)
        self.config(image=self.image)

class Tooltip(tp.Hovertip):
    """
    Tooltip which can be attached to buttons and more.
    """
    def __init__(self, anchor, text, hover_delay = 2000):
        super().__init__(anchor, text, hover_delay=hover_delay)

    def showcontents(self):
        label = tk.Label(self.tipwindow, text=self.text, 
                    justify=tk.LEFT, relief=tk.SOLID,
                    foreground="#000000", background="#ffffe0", borderwidth=1)
        label.pack()