from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Income, User
from schemas import IncomeCreate
from auth import get_current_user

router = APIRouter(prefix="/income", tags=["Income"])

@router.post("/add")
def add_income(income: IncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not income.category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category cannot be empty")
    new_income = Income(user_id=current_user.id, amount=income.amount, date=income.date,category=income.category)
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income

@router.get("/all")
def get_all_income(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Income).filter(Income.user_id == current_user.id).all()


@router.delete("/delete/{id:int}")
def delete_income_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    income_to_delete = db.query(Income).filter(Income.id == id and Income.user_id == current_user.id).first()
    if not income_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found")
    db.delete(income_to_delete)
    db.commit()
    return {"message": "Income deleted successfully"}

@router.put("/update/{id:int}")
def update_income(id: int, income: IncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    income_to_update = db.query(Income).filter(Income.id == id, Income.user_id == current_user.id).first()
    
    if not income_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found or doesn't belong to the current user")
    
    
    if income.amount:
        income_to_update.amount = income.amount
    if income.date:
        income_to_update.date = income.date
    if income.category:
        income_to_update.category = income.category
    
    
    db.commit()
    db.refresh(income_to_update)
    
    return income_to_update

