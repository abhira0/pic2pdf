import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import *

from .Backendpy import BackEnd
from .C4Upy import C4U
from .Statepy import State


class GUI(BackEnd):
    def __init__(self):
        # An empty state with all the initial values
        self.state = State()
        # Bind the state to GUI instance
        self.bindState(self.state)
        # Single function call to display the frontend
        self.display()

    def display(self):
        """Calls all functions to finaly get the GUI menu"""
        self.window_init()
        self.layer1Frame()

    def window_init(self):
        """TK Window is been instantiated with all initial configuration"""
        self.window = tk.Tk()
        self.window.title("ArgZ Pic2Pdf v{}".format(self.state.versionList[-1][0]))
        self.window.geometry(
            "{}x{}".format(C4U.grid_offsets["xscreen"], C4U.grid_offsets["yscreen"])
        )
        self.window.resizable(0, 0)

    def mySep(self, column: int, row: int):
        Separator(self.window).grid(column=column, row=row, sticky="ew")

    def crtFrm(self):
        return Frame(self.window)

    def crtBtn(self, name, frame, text: str, command, state="enabled", width=None):
        button = Button(frame, text=text, command=command, state=state, name=name)
        if width:
            button["width"] = width
        return button

    def crtLbl(self, given_frame, text, column: int, row: int, padx: str, pady: str):
        Label(given_frame, text=text).grid(
            column=column,
            row=row,
            padx=C4U.grid_offsets[padx],
            pady=C4U.grid_offsets[pady],
        )

    def gridConfig(self, given_frame, column, row, padx, pady, columnspan=None):
        given_frame.grid(
            column=column,
            row=row,
            padx=C4U.grid_offsets[padx],
            pady=C4U.grid_offsets[pady],
            columnspan=columnspan,
        )

    def layer1Frame(self):
        self.select_images = self.crtFrm()
        self.gridConfig(self.select_images, 0, 0, "x1", "y1", columnspan=2)
        self.callSelectImagesF()
        self.mySep(0, 1)  # -----------------------------------------------
        self.select_size = self.crtFrm()
        self.gridConfig(self.select_size, 0, 2, "x1", "y1")
        self.callSelectSizeF()
        self.callSelectOpSizeF()
        self.mySep(0, 3)  # -----------------------------------------------
        self.save_it = self.crtFrm()
        self.gridConfig(self.save_it, 0, 4, "x1", "y1")
        self.callSaveItF()
        self.mySep(0, 5)  # -----------------------------------------------
        self.create_it = self.crtFrm()
        self.gridConfig(self.create_it, 0, 6, "x1", "y1")
        self.callValidateF()
        self.mySep(0, 9)  # -----------------------------------------------
        self.note_it = self.crtFrm()
        self.gridConfig(self.note_it, 0, 10, "x1", "y1")
        self.callNotesF()
        self.window.mainloop()  # Loop ------------------------------------

    def callSelectImagesF(self):
        labels = [
            "Please select the image(s): ",
            "See selected images",
            "Selective Paste: ",
        ]
        self.crtLbl(self.select_images, labels[0], 0, 1, "x2", "y2")
        btn3 = self.crtBtn("btn3", self.select_images, "Select...", self.selImgBtn)
        btn3 = Button(self.select_images, text="Select...", command=self.selImgBtn)
        self.gridConfig(btn3, 1, 1, "x2", "y2")
        btn4 = self.crtBtn("btn4", self.select_images, labels[1], self.seeSelImgW)
        self.gridConfig(btn4, None, None, "x2", "y2", columnspan=2)
        part_print = Frame(self.select_images, name="part_print")
        self.gridConfig(part_print, 0, 3, "x2", "y2", columnspan=2)
        self.crtLbl(part_print, labels[2], 0, 0, "x2", "y2")
        part_regex = Entry(part_print, width=25, name="part_reg_entry")
        self.gridConfig(part_regex, 1, 0, "x2", "y2", columnspan=3)
        part_regex["state"] = "disable"
        self.enable_part_button = self.crtBtn(
            "ena_part", part_print, "Enable", self.enablePart
        )
        self.gridConfig(self.enable_part_button, 4, 0, "x2", "y2")

    def seeSelImgW(self):
        screen = tk.Tk()  # Screen / Window
        screen.geometry("900x300")  # screen size
        screen.resizable(width=0, height=0)  # Making it non resizable
        # left frame for table/treeview and (horizontal scroll bar[r8 now -n/a])
        lefty = Frame(screen)
        self.gridConfig(lefty, 0, 0, "x1", "y1")
        lefty.pack(side="left")
        # Treeview instance
        treetime = Treeview(lefty)
        treetime.pack(side=tk.TOP, fill=tk.X)
        # vertical scrollbar
        vbar = Scrollbar(screen, orient="vertical", command=treetime.yview)
        vbar.pack(side="right", fill="y")
        treetime.configure(yscrollcommand=vbar.set)
        # Columns
        treetime["columns"] = ("1", "2")
        treetime.column("1", width=50, minwidth=40, anchor=tk.W)
        treetime.column("2", width=800, minwidth=400, anchor=tk.W)
        treetime["show"] = "headings"
        treetime.heading("1", text="Sl. No.")
        treetime.heading("2", text="Path")
        for i in range(1, len(self.state.PATHS) + 1):
            treetime.insert("", "end", values=(str(i), self.state.PATHS[i - 1]))
        screen.mainloop()

    def callSelectSizeF(self):
        labels = ["Given photo type[ratio]: "]
        # --------- photo size
        self.crtLbl(self.select_size, labels[0], 0, 0, "x2", "y2")
        combo_photo = Combobox(self.select_size, width=40)
        combo_photo["values"] = [
            i + ": " + str(C4U.photo_sizes[i]) + "[in mm]"
            for i in [i for i in C4U.photo_sizes.keys()]
        ]
        self.gridConfig(combo_photo, 1, 0, "x2", "y2")
        # -------- custom photo size
        custom_frame = Frame(self.select_size, name="f_sel_pic_size")
        self.gridConfig(custom_frame, 0, 1, "x2", "y2", columnspan=2)
        custom_button = self.crtBtn(
            "custom_button",
            custom_frame,
            "Custom",
            lambda: self.callCustomSizeF(custom_frame),
        )
        self.gridConfig(custom_button, 0, 0, "x2", "y2", columnspan=2)

    def callSelectOpSizeF(self):
        labels = ["Required output paper size: "]
        # --------O/p size
        self.crtLbl(self.select_size, labels[0], 0, 3, "x2", "y2")
        combo_paper = Combobox(self.select_size, width=40)
        combo_paper["values"] = [
            i + ": " + str(C4U.paper_sizes[i]) + "[in mm]"
            for i in [i for i in C4U.paper_sizes.keys()]
        ]
        self.gridConfig(combo_paper, 1, 3, "x2", "y2")
        # --------custom o/p size
        custom_frame = Frame(self.select_size, name="f_sel_pap_size")
        self.gridConfig(custom_frame, 0, 4, "x2", "y2", columnspan=2)
        custom_button = self.crtBtn(
            "custom_button",
            custom_frame,
            "Custom",
            lambda: self.callCustomSizeF(custom_frame),
        )
        self.gridConfig(custom_button, 0, 0, "x2", "y2", columnspan=2)
        # ---------DPI
        dpi_frame = Frame(self.select_size, name="f_dpi")
        self.gridConfig(dpi_frame, None, 6, "x2", "y2", columnspan=2)
        Label(dpi_frame, text="Output DPI: ").grid()
        self.state.dpi_entry = Entry(dpi_frame, width=8)
        self.state.dpi_entry.insert(0, "300")
        self.gridConfig(self.state.dpi_entry, 1, 0, "x2", "y2")

    def callCustomSizeF(self, custom_frame):
        cus_button = custom_frame.children["custom_button"]
        cus_button["state"] = "disabled"

        width_entry = Entry(custom_frame, width=10, name="width_entry")
        self.gridConfig(width_entry, 2, 0, "x2", "y2")
        height_entry = Entry(custom_frame, width=10, name="height_entry")
        self.gridConfig(height_entry, 3, 0, "x2", "y2")

        prev_width = (
            self.state.pw if custom_frame._name == "f_sel_pic_size" else self.state.w
        )
        prev_height = (
            self.state.ph if custom_frame._name == "f_sel_pic_size" else self.state.h
        )
        show_width = prev_width if prev_width else "w"
        show_height = prev_height if prev_height else "h"
        width_entry.insert(0, show_width)
        height_entry.insert(0, show_height)
        save_button = self.crtBtn(
            "save_button",
            custom_frame,
            "Save",
            lambda: self.saveCustomDim(custom_frame),
            width=5,
        )
        self.gridConfig(save_button, 4, 0, "x2", "y2")
        cancel_button = self.crtBtn(
            "cancel_button",
            custom_frame,
            "X",
            lambda: self.closeCustomSize(custom_frame),
            width=2,
        )
        self.gridConfig(cancel_button, 5, 0, "x2", "y2")

    def callSaveItF(self):
        # --------- filename input
        self.crtLbl(self.save_it, "Choose a filename to save: ", 0, 0, "x2", "y2")
        self.state.op_filename_entry = Entry(self.save_it, width=40)
        self.gridConfig(self.state.op_filename_entry, 1, 0, "x2", "y2")
        # --------- checkbox :image or/and pdf
        self.crtLbl(self.save_it, "What do you want: ", 0, 1, "x2", "y2")
        checkFrame = Frame(self.save_it)
        self.gridConfig(checkFrame, 1, 1, "x2", "y2")
        self.state.imgchk, self.state.pdfchk = tk.IntVar(), tk.IntVar()

        ch1 = Checkbutton(checkFrame, text="Image", variable=self.state.imgchk)
        self.gridConfig(ch1, 0, 0, "x2", "y2")
        ch2 = Checkbutton(checkFrame, text="Pdf", variable=self.state.pdfchk)
        self.gridConfig(ch2, 1, 0, "x2", "y2")
        # --------- where to save
        self.crtLbl(self.save_it, "Choose a directory to save: ", 0, 2, "x2", "y2")
        btn5 = self.crtBtn("dir_button", self.save_it, "Choose...", self.chooseOPDirF)
        self.gridConfig(btn5, 1, 2, "x2", "y2")

    def chooseOPDirF(self):
        warnings = [["Warning while choosing", "Output directory path cannot be empty"]]
        dir_path = filedialog.askdirectory(
            initialdir=os.getcwd(), title="Select image(s)"
        )
        self.state.dirPATH = dir_path
        if self.state.dirPATH == "":
            messagebox.showwarning(*warnings[0])
        else:
            self.state.lab_ch_op = tk.Entry(self.save_it, width=60)
            self.gridConfig(self.state.lab_ch_op, 0, 3, "x2", "y2", 2)
            self.state.lab_ch_op.insert(0, self.state.dirPATH)
            self.state.lab_ch_op["state"] = "disabled"

    def callValidateF(self):
        def localGridConfig(given_frame, row, col, ipadx, ipady, padx, pady):
            given_frame.grid(
                ipady=ipady,
                ipadx=ipadx,
                row=row,
                column=col,
                pady=C4U.grid_offsets[pady],
                padx=C4U.grid_offsets[padx],
            )

        # --------- Validate button
        self.state.validate_button = self.crtBtn(
            "validate_button", self.create_it, "Validate", self.validation
        )
        localGridConfig(self.state.validate_button, 0, 0, 10, 5, "x2", "y2")
        # --------- Build button
        self.state.build_button = self.crtBtn(
            "build_button", self.create_it, "Build", self.builder, "disabled"
        )
        localGridConfig(self.state.build_button, 0, 1, 30, 5, "x2", "y2")
        # --------- Refresh
        refresh_button = self.crtBtn(
            "refresh_button", self.create_it, "Refresh", self.refreshwindow
        )
        localGridConfig(refresh_button, 0, 2, 10, 5, "x2", "y2")

    def callNotesF(self):
        """Displays the notes"""
        note1 = "All measurements are in mm"
        note2 = "Built by: ARG-Z"
        note3 = f"Version: {self.state.versionList[-1][0]}"
        self.crtLbl(self.note_it, note1, 0, 0, "x2", "y2")
        self.crtLbl(self.note_it, note2, 0, 1, "x2", "y2")
        self.crtLbl(self.note_it, note3, 0, 3, "x2", "y2")
