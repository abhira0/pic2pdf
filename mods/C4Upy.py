class C4U:
    """Constants for You: A class of constants"""

    # sizes (w*h) are in mm
    paper_sizes = {"A4": (210, 297), "A5": (148, 210)}
    grid_offsets = {
        "xscreen": 465,
        "yscreen": 580,
        "x1": 20,
        "y1": 10,
        "x2": 2,
        "y2": 2,
    }
    photo_sizes = {
        "Indian Passport Size": (35, 45),
        "Indian Stamp Size": (20, 25),
        "Indian SSLC Size": (25, 25),
        "Indian Normal Stamp size": (25, 30),
        "Indian Pan Card Size": (25, 35),
        "Indian Passport Form Size": (35, 35),
    }
    # photo_borders dimensions are in pixels and not in mm
    photo_borders = {
        "Indian Passport Size": (25, 25),
        "Indian Stamp Size": (20, 20),
        "Indian SSLC Size": (15, 15),
        "Indian Normal Stamp size": (20, 20),
        "Indian Pan Card Size": (20, 20),
        "Indian Passport Form Size": (25, 25),
    }
