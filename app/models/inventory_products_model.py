from pydantic import BaseModel

class InventoryProducts (BaseModel):

 id: int
quantity: int
idInventorySite: int
idProduct: int
