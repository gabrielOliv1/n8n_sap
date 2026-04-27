from enum import Enum


class PurchaseType(str, Enum):
    SPOT = "SPOT"
    PLANNED = "PLANNED"
    CONTRACT = "CONTRACT"
    SERVICE = "SERVICE"
    STO = "STO"


#
