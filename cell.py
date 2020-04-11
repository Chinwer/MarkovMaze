from enum import Enum

class Cell(Enum):
    PATH = 0
    BLOCK = 1
    TRAP = 2
    START = 3
    END = 4
