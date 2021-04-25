class State:
    def __init__(self) -> None:
        self.PATHS = []
        self.dirPATH = ""
        self.pw = 0  # pic width
        self.w = 0  # window screen width
        self.ph = 0  # pic height
        self.h = 0  # window screen height
        self.filename = ""
        self.validity = 0
        self.DPI_value = 300  # default DPI
        self.built_flag = 0
        self.photo_type = ""
        self.selective_paste_flag = False
        self.versionList = [
            ["21.1.7", "Initial Version"],
            ["21.1.16", "Code reformat"],
            ["21.1.18", "Code reformat"],
            ["21.1.20", "Code reformat"],
            ["21.1.23", "Code reformat"],
            ["21.1.24", "Added Selective Paste"],
        ]
        self.copies = []
        self.customCopies = 0
