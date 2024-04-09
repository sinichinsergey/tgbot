from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from models import Sale
from schemas import SaleCreate


def get_sales(
        db: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None):
    query = db.query(Sale)
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    query = query.order_by(Sale.sale_date, Sale.product_name)
    return query.all()


def create_sale(db: Session, sale: SaleCreate):
    _sale = Sale(
        sale_date=sale.sale_date,
        product_name=sale.product_name,
        quantity=sale.quantity,
        price=sale.price)
    db.add(_sale)
    db.commit()
    db.refresh(_sale)
    return _sale
