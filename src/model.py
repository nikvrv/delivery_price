from dataclasses import dataclass
from enum import Enum


class Size(Enum):
    BIG = "big"
    SMALL = "small"


class WorkloadRate(Enum):
    VERY_HIGH = 1.6
    HIGH = 1.4
    UPPER_MEDIUM = 1.2
    OTHER = 1


@dataclass
class Cargo:
    size: Size  # 'big' or 'small'
    fragility: bool  # True or False


class CalculatePriceException(Exception):
    """Can't calculate price'"""
    pass
