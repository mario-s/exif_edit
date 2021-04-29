"""
GUI of the application.
"""

import sys
import logging
import tkinter as tk
import tkinter.filedialog as filedialog

from tkinter import DISABLED, NORMAL
from tkinter import ttk
from idlelib import tooltip as tp
from tksheet import Sheet

from PIL import ImageTk as itk
from PIL import Image

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
            "open file " + self.__acc("O"), self.__open)
        btn_open.pack(side=tk.LEFT, padx=2, pady=5)

        btn_save = ToolbarButton(toolbar, self.__icon("save-file.png"),
            "save exif data " + self.__acc("S"), self.__save)
        btn_save.pack(side=tk.LEFT, padx=2, pady=5)

        btn_exit = ToolbarButton(toolbar, self.__icon("exit.png"),
            "exit "+ self.__acc("W"), self.__quit)
        btn_exit.pack(side=tk.LEFT, padx=2, pady=5)

        sep = ttk.Separator(toolbar, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, padx=2, pady=5, fill='y')

        btn_add = ToolbarButton(toolbar, self.__icon("add-row.png"),
            "add a row", self.__add_row)
        btn_add.pack(side=tk.LEFT, padx=2, pady=5)

        self.btn_insert = ToolbarButton(toolbar, self.__icon("insert.png"),
            "insert a row after selected", self.__insert_row, True)
        self.btn_insert.pack(side=tk.LEFT, padx=2, pady=5)

        self.btn_rm = ToolbarButton(toolbar, self.__icon("delete-row.png"),
            "remove selected row", self.__remove_row, True)
        self.btn_rm.pack(side=tk.LEFT, padx=2, pady=5)

        self.btn_sort = ToolbarButton(toolbar, self.__icon("sort.png"),
            "sort table", self.__sort_table, True)
        self.btn_sort.pack(side=tk.LEFT, padx=2, pady=5)

        sep = ttk.Separator(toolbar, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, padx=2, pady=5, fill='y')

        self.btn_loc = ToolbarButton(toolbar, self.__icon("world.png"),
            "show location " + self.__acc("L"), self.__open_location, True)
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

        self.__update_buttons()
        #ensure that window has focus again
        self.focus_set()
        self.__center()

    def single_select(self, event):
        print(event)

    def drag_select_rows(self, event):
        self.__update_row_buttons(event)

    def begin_edit_cell(self, event):
        self.mediator.begin_edit_cell((event[0], event[1]))

    def end_edit_cell(self, event):
        self.mediator.end_edit_cell((event[0], event[1]))
        self.__update_location_button()

    def deselect(self, event):
        self.__update_row_buttons(event)

    def cell_select(self, event):
        self.__update_row_buttons(event)

    def row_select(self, event):
        self.__update_row_buttons(event)

    def __add_row(self):
        self.mediator.add_row()

    def __insert_row(self):
        self.mediator.insert_row()

    def __remove_row(self):
        self.mediator.remove_row()
        self.__update_location_button()

    def __update_row_buttons(self, event):
        enabled = self.mediator.can_remove_row(event)
        self.btn_insert.toggle_state(enabled)
        self.btn_rm.toggle_state(enabled)

    def __sort_table(self):
        pass

    def __update_buttons(self):
        self.btn_sort.toggle_state(self.mediator.has_rows())
        self.btn_loc.toggle_state(self.mediator.has_location())

    def start(self):
        """
        This method starts the GUI and places it in the center of the screen.
        """
        self.__center()
        self.mainloop()

    def __center(self):
        #https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        self.eval('tk::PlaceWindow . center')

    def __open(self, event = None):
        name = filedialog.askopenfilename()
        self.load_image(name)

    def __save(self, event = None):
        self.mediator.save_exif()

    def __open_location(self, event = None):
        self.mediator.show_location()

    @classmethod
    def __quit(cls, event = None):
        sys.exit(0)

class ToolbarButton(tk.Button):
    """
    Button for the toolbar.
    """
    def __init__(self, anchor, icon, tooltip, cmd, disabled=False):
        self.icon = icon.convert("RGBA")
        self.image = itk.PhotoImage(self.icon)
        self.overlay = Image.new('RGBA', icon.size, (255, 255, 255, 0))
        super().__init__(anchor, image=self.image, relief=tk.FLAT, command=cmd)
        Tooltip(self, text=tooltip)
        if disabled:
            self.disable()

    def toggle_state(self, enabled=True):
        """
        This method changes the state of the button:
        If enable=True the button will be enaled, else disabled.
        """
        if enabled:
            self.enable()
        else:
            self.disable()

    def disable(self):
        """
        Extended method to disable the button, it also changes the icon.
        """
        self.config(state=DISABLED)
        img = Image.blend(self.icon, self.overlay, 0.3)
        self.__config_image(itk.PhotoImage(img))

    def enable(self):
        """
        Extended method to enable the button, it restores the original icon.
        """
        self.config(state=NORMAL)
        self.__config_image(itk.PhotoImage(self.icon))

    def __config_image(self, img):
        self.image = img
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
