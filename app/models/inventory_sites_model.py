from pydantic import BaseModel


class InventorySites (BaseModel):
    
    idInventory: int
    idSite: int
