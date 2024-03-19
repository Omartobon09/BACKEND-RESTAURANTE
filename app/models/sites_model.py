from pydantic import BaseModel


class Sites(BaseModel):
    Name: str
    Address: str
