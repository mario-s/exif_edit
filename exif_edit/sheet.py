from access import Reader
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
        
        self.__add_sheet__()

    def __add_sheet__(self):
        self.sheet = Sheet(self.frame, page_up_down_select_row = True,
            headers = ["Key", "Value"],
            height = 500, width = 600)
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.__add_bindings__()

    def __add_bindings__(self):
        self.sheet.enable_bindings(("single_select", 
                                         "drag_select",   
                                         "row_select",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
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
                                    ("shift_row_select", self.shift_select_rows),
                                    ("shift_column_select", self.shift_select_columns),
                                    ("drag_select_columns", self.drag_select_columns),
                                    ("deselect", self.deselect)
                                    ])
        

    def read_exif(self, img_path):
        self.reader = Reader(img_path)
        self.sheet.set_sheet_data(self.reader.list_of_lists())
        self.sheet.set_all_column_widths(250)
        self.__add_image__(img_path)

    def __add_image__(self, img_path):
        render = ImageTk.PhotoImage(Image.open(img_path))
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
        print (event, self.sheet.get_selected_cells())

    def rc(self, event):
        print (event)
        
    def cell_select(self, response):
        print (response)

    def shift_select_cells(self, response):
        print (response)

    def row_select(self, response):
        print (response)

    def shift_select_rows(self, response):
        print (response)

    def shift_select_columns(self, response):
        print (response)

    def drag_select_columns(self, response):
        pass


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
