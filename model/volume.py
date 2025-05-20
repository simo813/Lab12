from dataclasses import dataclass

from model.retailer import Retailer


@dataclass
class Volume:
    node: Retailer
    volume: int