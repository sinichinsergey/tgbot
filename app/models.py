from sqlalchemy import Column, Integer, Date, String, Float

from database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    sale_date = Column(Date)
    product_name = Column(String)
    quantity = Column(Float)
    price = Column(Float)
