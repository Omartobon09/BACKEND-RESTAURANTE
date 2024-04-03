from pydantic import BaseModel


class Inventory (BaseModel):
    ItemName: str
    Quantity: int
    Unit: str
