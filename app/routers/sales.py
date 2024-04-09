from datetime import date
from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from crud import sales as crud_sales
from schemas import SaleCreate
from database import SessionLocal

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_all_sales(
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        db: Session = Depends(get_db)):
    _sales = crud_sales.get_sales(db, start_date=start_date, end_date=end_date)
    return _sales


@router.post("/create", response_model=SaleCreate)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        _sale = crud_sales.create_sale(db, sale=sale)
        return _sale
    except Exception as _ex:
        raise HTTPException(status_code=400, detail=str(_ex))
