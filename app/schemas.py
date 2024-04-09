from datetime import date

from pydantic import BaseModel


class SaleCreate(BaseModel):
    sale_date: date
    product_name: str
    quantity: float
    price: float
