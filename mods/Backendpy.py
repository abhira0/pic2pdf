import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import *

from PIL import Image, ImageDraw

from .Statepy import State
from .C4Upy import C4U

"""
Online References
1> To calculate the pixels
    https://www.pixelcalculator.com/index.php?round=&FORM=1&DP=1&FA=&lang=en&mm1=35&mm2=45&dpi1=300&sub1=+calculate+#a1
2>
"""


class BackEnd:
    def bindState(self, given_state: State) -> None:
        """Bind the particular state to the Backend instance

        Args:
            given_state (State): A state required to bind to the GUI instance
        """
        self.state = given_state

    def tryExcept(self, fun):
        try:
            fun()
        except:
            pass

    def selImgBtn(self):
        PATHs = list(
            filedialog.askopenfilenames(
                initialdir=os.getcwd(),
                title="Select image(s)",
                filetypes=[("Images", [".png", ".jpg", ".jpeg", ".jfif"])],
            )
        )
        if len(PATHs) != 0:
            self.state.PATHS = sorted(list(set(self.state.PATHS + PATHs)))
            print(f"\t[i] {len(PATHs)} Images selected")

    def enablePart(self):
        if self.enable_part_button["text"] == "Enable":
            self.enable_part_button["text"] = "Disable"
            entry = self.select_images.children["part_print"].children["part_reg_entry"]
            entry["state"] = "enable"
            print(f"\t[i] Selective Paste Enabled")
        else:
            self.enable_part_button["text"] = "Enable"
            entry = self.select_images.children["part_print"].children["part_reg_entry"]
            entry.delete(0, "end")
            entry["state"] = "disable"
            self.state.selective_paste_flag = False
            print(f"\t[i] Selective Paste Disabled")

    def getBorderSize(self):
        try:
            pic_border = C4U.photo_borders[self.state.photo_type]
        except:
            pic_border = C4U.photo_borders["Indian Passport Size"]
            print(f"\t[i] Border size if defaulted to '{pic_border}'")
        return pic_border

    def putBorder(self, pic):
        # print(f"\t[i] Putting borders for the pictures")
        w, h = pic.size  # width, height
        pic_border = self.getBorderSize()

        image_with_border = Image.new(
            "RGB",
            (w + 2 * pic_border[0], h + 2 * pic_border[1]),
            (255, 255, 255, 255),
        )
        position = (pic_border[0], pic_border[1])
        image_with_border.paste(pic, position)
        w, h = image_with_border.size
        drawlplus = ImageDraw.Draw(image_with_border)
        # draw corner lines on the image tile
        drawlplus.line((0, 0, 0, 10), fill=0, width=1)
        drawlplus.line((0, 0, 10, 0), fill=0, width=1)
        drawlplus.line((0, h - 1, 0, h - 10 - 1), fill=0, width=1)
        drawlplus.line((0, h - 1, 10, h - 1), fill=0, width=1)
        drawlplus.line((w - 1, 0, w - 1, 10), fill=0, width=1)
        drawlplus.line((w - 1, 0, w - 10 - 1, 0), fill=0, width=1)
        drawlplus.line((w - 1, h - 1, w - 10 - 1, h - 1), fill=0, width=1)
        drawlplus.line((w - 1, h - 1, w - 1, h - 10 - 1), fill=0, width=1)
        return image_with_border

    def parseReg(self):
        part_print_children = self.select_images.children["part_print"].children
        reg = part_print_children["part_reg_entry"].get()
        l = [i.split(":") for i in reg.split(";")]
        for i in l:
            if len(i) != 2:
                print(f"[!] Reg-Parse Error: There are more number of ':'")
                raise Exception("Reg-Parse Error")
            i[0] = int(i[0].strip())
            els = i[1].split(",")
            nums = []
            for k in els:
                try:
                    nums.append(int(k.strip()))
                except:
                    if "-" in k:
                        a, b = map(int, k.split("-"))
                        nums += list(range(a, b + 1))
            i[1] = list(set(nums))
        return l

    def makeFullCopies(self):
        def getPicNum(pw, ph, w, h):
            """Return the xpics, ypics and total number of pics in a page"""
            return (
                int((w - 40) / pw),  # xpics
                int((h - 40) / ph),  # ypics
                int((w - 40) / pw) * int((h - 40) / ph),  # total
            )

        def getPixel(side):
            return int(side * DPI_value / 25.4)

        paths = self.state.PATHS
        DPI_value = self.state.dpi_entry_value
        pw = getPixel(self.state.pw)
        ph = getPixel(self.state.ph)
        pic_border = self.getBorderSize()
        # Adding gutter pixels
        pw, ph = (pw + 2 * pic_border[0], ph + 2 * pic_border[1])
        w = getPixel(self.state.w)
        h = getPixel(self.state.h)
        xpics, ypics, totpix = getPicNum(pw, ph, w, h)
        if totpix < getPicNum(pw, ph, h, w)[2]:
            w, h = h, w  # swap dimensions
            print(
                f"\t[i] Change in page orientation to accommodate pics from '{totpix}' to '{getPicNum(pw, ph, w, h)[2]}'"
            )
            xpics, ypics, totpix = getPicNum(pw, ph, w, h)

        a4 = Image.new("RGB", (w, h), (255, 255, 255, 255))
        positions = [
            (i, j)
            for i in range(int(0.5 * (w - pw * xpics)), w, pw)
            for j in range(int(0.5 * (h - ph * ypics)), h, ph)
            if (w - 0.5 * (w - pw * xpics)) - i >= pw
            and (h - 0.5 * (h - ph * ypics)) - j >= ph
        ]
        totpaths = len(paths)
        # print("positions: " + str(positions))
        li = [int(totpix / totpaths) + totpix % totpaths]
        for j in range(1, totpaths):
            li.append(int(totpix / totpaths))
        # Mention number of copies if not equal
        # li = [8,8,3,3,3,3]
        def full():
            print(f"\t[i] Entering into Full Copy mode since no regex is given")
            i = 0
            kkk = 0
            for j in li:
                pic = Image.open(paths[kkk])
                pic = pic.resize(
                    (
                        int(self.state.pw * DPI_value / 25.4),
                        int(self.state.ph * DPI_value / 25.4),
                    )
                )
                pic = self.putBorder(pic)
                kkk += 1
                for k in range(j):
                    a4.paste(pic, positions[i])
                    i += 1

        def partial():
            print(f"\t[i] Entering into Selective Paste Mode.")
            li = self.parseReg()
            dikt = {i: -1 for i in range(totpix)}
            for i in li:
                a, b = i
                for c in b:
                    dikt[c - 1] = a - 1
            i = 0
            for i, j in dikt.items():
                # i: pic position in paper
                # j: image path index
                if j != -1 and j >= 0 and j < len(paths):
                    if i >= 0 and i < len(positions):
                        pic = Image.open(paths[j])
                        pic = pic.resize(
                            (
                                int(self.state.pw * DPI_value / 25.4),
                                int(self.state.ph * DPI_value / 25.4),
                            )
                        )
                        pic = self.putBorder(pic)
                        a4.paste(pic, positions[i])

        def save(extension):
            a4.save(self.state.filename + extension)
            print(f"\t[i] Output file save as: {self.state.filename + extension}")

        partial() if self.state.selective_paste_flag else full()
        save(".jpg") if self.state.imgchk.get() else None
        save(".pdf") if self.state.pdfchk.get() else None
        self.state.built_flag = 1

    def closeCustomSize(self, custom_frame):
        children = custom_frame.children
        children["custom_button"]["state"] = "enabled"
        try:
            children["width_entry"].grid_remove()
            children["height_entry"].grid_remove()
        except:
            pass
        children["save_button"].grid_remove()
        children["cancel_button"].grid_remove()
        self.clearWH(custom_frame)
        print(
            f"\t[i] Cleared: pw: '{self.state.pw}', ph: '{self.state.ph}',"
            f"w: '{self.state.w}', h: '{self.state.h}'"
        )

    def saveCustomDim(self, custom_frame):
        warnings = [
            [
                "Non-Positive is unacceptable",
                "Enter a positive number(integer/decimal)",
            ],
            ["Out of range", "Range: 1-999 mm"],
            ["Not a number", "Enter a positive number(integer/decimal)"],
        ]
        save_button = custom_frame.children["save_button"]
        width_entry = custom_frame.children["width_entry"]
        height_entry = custom_frame.children["height_entry"]
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            if width <= 0 or height <= 0:
                messagebox.showwarning(*warnings[0])
                return
            if width >= 1000 or height >= 1000:
                messagebox.showwarning(*warnings[1])
                return
        except:
            messagebox.showwarning(*warnings[2])
            return
        if custom_frame._name == "f_sel_pic_size":
            self.state.pw, self.state.ph = width, height
        else:
            self.state.w, self.state.h = width, height
        width_entry.grid_remove()
        height_entry.grid_remove()
        save_button["text"] = f"Saved: {width}x{height} mm^2"
        save_button["width"] = 35
        save_button["state"] = tk.DISABLED
        siblings = custom_frame.master.children
        combobox = (
            siblings["!combobox"]
            if custom_frame._name == "f_sel_pic_size"
            else siblings["!combobox2"]
        )
        combobox.set("")
        print(
            f"\t[i] Saved: pw: '{self.state.pw}', ph: '{self.state.ph}',"
            f"w: '{self.state.w}', h: '{self.state.h}'"
        )

    def clearWH(self, custom_frame):
        flag = 1 if custom_frame._name == "f_sel_pic_size" else 0
        if flag:
            self.state.pw = 0
            self.state.ph = 0
        else:
            self.state.w = 0
            self.state.h = 0

    def validation(self):
        state_it = self.crtFrm()
        state_it.grid(column=0, row=8, pady=2, padx=C4U.grid_offsets["x1"])
        lab0 = Label(state_it, text="Processing...")
        lab0.grid(ipadx=5, pady=C4U.grid_offsets["y2"], padx=C4U.grid_offsets["x2"])
        msg = []

        def v_selectImage():
            if len(self.state.PATHS) == 0:
                msg.append("Select at least one image")
            warning = "One of the given paths does not exist. Check cmd-line"
            for i in self.state.PATHS:
                if not os.path.exists(i):
                    msg.append(warning) if warning not in msg else None
                    print(f"[!] The following media path does not exist: '{i}'")
            print(f"\t[i] Media Paths: {self.state.PATHS}")

        def v_selective():
            part_print_children = self.select_images.children["part_print"].children
            if part_print_children["ena_part"]["text"] == "Disable":
                reg = part_print_children["part_reg_entry"].get()
                if reg == "":
                    msg.append("Selective Paste has Empty string")
                    self.enablePart()
                else:
                    try:
                        l = self.parseReg()
                        self.state.selective_paste_flag = True
                        print(f"\t[i] Parsed regex: {l}")
                    except:
                        msg.append("Regex Parsing Error")

        def v_photoSize():
            if (self.state.pw == 0) and (self.state.ph == 0):
                try:
                    self.state.photo_type = (
                        self.select_size.children["!combobox"].get().split(":")[0]
                    )
                    photo_size = C4U.photo_sizes[self.state.photo_type]
                    self.state.pw, self.state.ph = photo_size
                    print(
                        f"\t[i] Photo_type: {self.state.photo_type}, Photo_size: {photo_size}"
                    )
                except:
                    msg.append("Select the photo type/size")
            else:
                print(f"\t[i] Custom photo_size: {(self.state.pw, self.state.ph)}")

        def v_paperSize():
            if (self.state.w == 0) and (self.state.h == 0):
                try:
                    btn1_value = (
                        self.select_size.children["!combobox2"].get().split(":")[0]
                    )
                    paper_size = C4U.paper_sizes[btn1_value]
                    self.state.w = paper_size[0]
                    self.state.h = paper_size[1]
                    print(f"\t[i] Paper_type: {btn1_value}, Paper_size: {paper_size}")
                    del paper_size, btn1_value
                except:
                    msg.append("Select the output paper size")
            else:
                print(f"\t[i] Custom paper_size: {(self.state.w, self.state.h)}")
            # --------- pic < paper
            if self.state.pw * self.state.ph > self.state.w * self.state.h:
                msg.append("Paper size must be greater than pic size")

        def v_dpiEntry():
            try:
                self.state.dpi_entry_value = int(self.state.dpi_entry.get())
            except:
                msg.append("Output DPI must be an integer")
            if self.state.dpi_entry_value <= 0:
                self.state.dpi_entry_value = 300
                self.state.dpi_entry.delete(0, "end")
                self.state.dpi_entry.insert(0, "300")
                msg.append("Output DPI must be greater than 0")
            print(f"\t[i] Current DPI: {self.state.dpi_entry_value}")

        def v_filename():
            filename = str(self.state.op_filename_entry.get())
            if filename == "":
                msg.append("Provide the output filename")
            else:
                self.state.filename = filename.replace("/", "\\")
            print(f"\t[i] Filename: '{self.state.filename}'")

        def v_checkbox():
            try:
                if (self.state.imgchk.get() == 0) and (self.state.pdfchk.get() == 0):
                    msg.append("Select at least one output format")
                print(
                    f"\t[i] ImageFlag: {self.state.imgchk.get()}, PdfFlag: {self.state.pdfchk.get()}"
                )
            except:
                msg.append("Select at least one output format")

        def v_destinationPath():
            if self.state.dirPATH == "":
                msg.append("Select destination path")
            elif not os.path.exists(self.state.dirPATH):
                self.state.dirPATH = ""
                msg.append("Destination path does not exist")
            print(f"\t[i] O/P Directory: '{self.state.dirPATH}'")

        print("--------------- Validation ---------------")
        v_selectImage()
        v_selective()
        v_photoSize()
        v_paperSize()
        v_dpiEntry()
        v_filename()
        v_checkbox()
        v_destinationPath()
        print("------------------------------------------")
        if len(msg) == 0:
            self.state.validity = True
            lab0["text"] = "Good to go..."
            messagebox.showinfo("Great", "Good to go...")
            self.state.validate_button["state"] = tk.DISABLED
            self.state.build_button["state"] = tk.NORMAL
        else:
            lab0["text"] = "Check again and validate"
            messagebox.showwarning(
                "Warnings",
                "\n".join(["{}> {}".format(i + 1, msg[i]) for i in range(len(msg))]),
            )
        lab0.grid_remove()
        state_it.destroy()

    def builder(self):
        print("---------------- Building ----------------")
        build_it = self.crtFrm()
        build_it.grid(column=0, row=7, pady=2, padx=C4U.grid_offsets["x1"])
        lab0 = Label(build_it, text="Building...")
        lab0.grid(
            columnspan=10,
            ipadx=5,
            pady=C4U.grid_offsets["y2"],
            padx=C4U.grid_offsets["x2"],
        )
        self.makeFullCopies()
        lab0.grid_remove()
        if self.state.built_flag == 0:
            messagebox.showerror(
                "S0RTA Bug", "There was an error\nPlease contact the dev"
            )
        else:
            self.state.built_flag = 0
            messagebox.showinfo("Job is done", "Successfully saved at the location :)")
        self.state.validate_button["state"] = "normal"
        self.state.build_button["state"] = "disabled"
        build_it.destroy()
        print("------------------------------------------")

    def refreshwindow(self):
        print("--------------- Refreshing ---------------")
        self.state.PATHS = []
        self.state.dirPATH = ""
        self.state.pw = 0
        self.state.w = 0
        self.state.ph = 0
        self.state.h = 0
        self.state.filename = ""
        self.state.validity = 0
        self.state.built_flag = 0
        self.state.dpi_entry_value = 300
        self.state.selective_paste_flag = False
        self.select_size.children["!combobox"].set("")
        self.select_size.children["!combobox2"].set("")
        self.state.imgchk.set(0)
        self.state.pdfchk.set(0)
        self.state.validate_button["state"] = "normal"
        self.state.build_button["state"] = "disabled"
        self.state.dpi_entry.delete(0, "end")
        self.state.dpi_entry.insert(0, "300")
        if self.enable_part_button["text"] == "Disable":
            self.enablePart()
        self.state.op_filename_entry.delete(0, "end")
        for i, j in self.select_size.children.items():
            if "f_sel_" in i and "cancel_button" in j.children:
                j.children["cancel_button"].invoke()

        def fun4():
            self.state.lab_ch_op.grid_remove()

        self.tryExcept(fun4)
        print("------------------------------------------")
