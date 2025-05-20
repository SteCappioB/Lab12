from dataclasses import dataclass

from model.retailer import Retailer


@dataclass
class Arco:
    r1: Retailer
    r2: Retailer
    peso: int
