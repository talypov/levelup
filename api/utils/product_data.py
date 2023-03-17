from dataclasses import dataclass


@dataclass(init=False)
class ProductData:
    product_no: str
    name: str
    description: str
    r_state: str
    type: str
    qty: int = 1

    def __init__(self, data: {}) -> None:
        self.product_no = data.get('product_no', None)
        self.name = data.get('name', None)
        self.description = data.get('description', None)
        self.r_state = data.get('r_state', None)
        self.type = data.get('type', None)
        self.qty = data.get('qty', None)
