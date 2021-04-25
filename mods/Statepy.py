class State:
    """A class containing all the initial setup variables required to bootup the program"""

    def __init__(self) -> None:
        self.PATHS = []  # Paths of the images
        self.dirPATH = ""  # Path for o/p directory
        self.pw = 0  # Pic width
        self.w = 0  # Window screen width
        self.ph = 0  # Pic height
        self.h = 0  # Window screen height
        self.filename = ""  # O/p filename
        self.validity = 0  # Flag: Valid bit not set
        self.DPI_value = 300  # default DPI
        self.built_flag = 0  # Flag: whether the program built reuired o/p
        self.photo_type = ""  # Type of the pic selected by user
        self.selective_paste_flag = False  # Flag: Regex enabler
        self.versionList = [
            ["21.1.7", "Initial Version"],
            ["21.1.16", "Code reformat"],
            ["21.1.18", "Code reformat"],
            ["21.1.20", "Code reformat"],
            ["21.1.23", "Code reformat"],
            ["21.1.24", "Added Selective Paste"],
        ]
