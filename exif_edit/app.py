from math import e
from image_io import Mediator
from tksheet import Sheet

import tkinter as tk
import tkinter.filedialog as filedialog

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
        sheet = Sheet(self.frame, page_up_down_select_row = True,
            headers = ["Key", "Value"],
            height = 600, width = 600)
        sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.mediator = Mediator(sheet) 
        self.sheet = sheet
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
                                    ("row_select", self.row_select),
                                    ("deselect", self.deselect)
                                    ])
        
    def __add_commands(self):
        left_cmd_frame = tk.Frame(self.frame, borderwidth=2)
        left_cmd_frame.grid(row = 1, column = 0, sticky = "nswe")
        btn_add = tk.Button(left_cmd_frame, text="+", command=self.mediator.add_row)
        btn_add.pack(padx=5, pady=10, side=tk.LEFT)
        self.btn_rm = tk.Button(left_cmd_frame, text="-", command=self.mediator.remove_row, 
            state=tk.DISABLED)
        self.btn_rm.pack(padx=5, pady=10, side=tk.LEFT)

        right_cmd_frame = tk.Frame(self.frame, borderwidth=2)
        right_cmd_frame.grid(row = 1, column = 1, sticky = "nswe")
        btn_exit = tk.Button(right_cmd_frame, text="exit", command=self.destroy)
        btn_exit.pack(padx=5, pady=10, side=tk.RIGHT)
        btn_save = tk.Button(right_cmd_frame, text="save", command=self.mediator.save_exif)
        btn_save.pack(padx=5, pady=10, side=tk.RIGHT)

    def load_image(self, img_path):
        self.mediator.append_exif(img_path)
        image = self.mediator.read_image(img_path)
        label = tk.Label(self.frame, image=image)
        label.image = image
        label.grid(row = 0, column = 1, sticky = "nswe")        

    def save_image(self):
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
        
    def cell_select(self, event):
        self.__change_button_state(event)

    def row_select(self, event):
        self.__change_button_state(event)

    def __change_button_state(self, event):
        name = event[0]
        if name == "select_row":
            self.btn_rm.config(state=tk.NORMAL)
        elif name == "deselect_all" or name == "select_cell":
            self.btn_rm.config(state=tk.DISABLED)

