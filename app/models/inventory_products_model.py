from pydantic import BaseModel


class InventoryProducts (BaseModel):

    quantity: int
idInventorySite: int
idProduct: int
