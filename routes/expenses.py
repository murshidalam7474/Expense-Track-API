from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Income, Expense, User
from schemas import IncomeCreate, ExpenseCreate
from auth import get_current_user

router = APIRouter()

# Income Routes
income_router = APIRouter(prefix="/income", tags=["Income"])

@income_router.post("/add")
def add_income(income: IncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not income.category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")
    new_income = Income(user_id=current_user.id, amount=income.amount, date=income.date,category=income.category)
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income

@income_router.get("/all")
def get_all_income(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Income).filter(Income.user_id == current_user.id).all()

# Expense Routes
expense_router = APIRouter(prefix="/expenses", tags=["Expenses"])

@expense_router.post("/add")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    new_expense = Expense(user_id=current_user.id, amount=expense.amount, date=expense.date,category=expense.category)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@expense_router.get("/all")
def get_all_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Expense).filter(Expense.user_id == current_user.id).all()

# Include Routers
router.include_router(income_router)
router.include_router(expense_router)
