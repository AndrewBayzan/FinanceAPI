from enum import Enum

class CommissionSource(str, Enum):
    SOURCE = "source"
    DESTINATION = "destination"

    