from math import e
from image_io import ExifReader, ImageReader
from tksheet import Sheet
from PIL import Image, ImageTk

import tkinter as tk
import os
import sys


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, className='exif_edit')
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.frame = tk.Frame(self)
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        
        self.__add_sheet()

    def __add_sheet(self):
        self.sheet = Sheet(self.frame, page_up_down_select_row = True,
            headers = ["Key", "Value"],
            height = 500, width = 600)
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.__add_bindings()
        self.__add_commands()

    def __add_bindings(self):
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
                                    ("shift_cell_select", self.shift_select_cells),
                                    ("row_select", self.row_select),
                                    ("shift_column_select", self.shift_select_columns),
                                    ("deselect", self.deselect)
                                    ])
        
    def __add_commands(self):
        self.cmd_frame = tk.Frame(self.frame, borderwidth=2)
        self.cmd_frame.grid(row = 1, column = 0, sticky = "nswe")

        self.btn_add = tk.Button(self.cmd_frame, text="+")
        self.btn_add.pack(padx=5, pady=10, side=tk.LEFT)
        self.btn_rm = tk.Button(self.cmd_frame, text="-", state=tk.DISABLED)
        self.btn_rm.pack(padx=5, pady=10, side=tk.LEFT)

    def read_exif(self, img_path):
        self.reader = ExifReader(img_path)
        self.sheet.set_sheet_data(self.reader.list_of_lists())
        self.sheet.set_all_column_widths(250)
        self.__add_image(img_path)

    def __add_image(self, img_path):
        img_reader = ImageReader()
        render = ImageTk.PhotoImage(img_reader.read(img_path))
        self.label = tk.Label(self.frame, image=render)
        self.label.image = render
        self.label.grid(row = 0, column = 1, sticky = "nswe")

    def save_exif(self):
        data = self.sheet.get_sheet_data()
        print(data)

    def single_select(self, event):
        print(event)
    
    def begin_edit_cell(self, event):
        print(event)  

    def end_edit_cell(self, event):
        print(event)

    def mouse_motion(self, event):
        region = self.sheet.identify_region(event)
        row = self.sheet.identify_row(event, allow_end = False)
        column = self.sheet.identify_column(event, allow_end = False)
        print (region, row, column)

    def deselect(self, event):
        self.__change_button_state(event)

    def rc(self, event):
        print (event)
        
    def cell_select(self, event):
        self.__change_button_state(event)

    def shift_select_cells(self, event):
        print (event)

    def row_select(self, event):
        self.__change_button_state(event)

    def shift_select_columns(self, event):
        print (event)

    def __change_button_state(self, event):
        name = event[0]
        if name == "select_row":
            self.btn_rm.config(state=tk.NORMAL)
        elif name == "deselect_all" or name == "select_cell":
            self.btn_rm.config(state=tk.DISABLED)



def img_path():
    img_path = os.path.realpath('./test/resources/lookup.jpg')
    args_len = len(sys.argv) - 1
    if args_len > 0:
        img_path = os.path.realpath(sys.argv[1])
    return img_path


app = App()
app.read_exif(img_path())
app.save_exif()
app.mainloop()
