from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Income, Expense, Budget, User
from schemas import IncomeCreate, ExpenseCreate, BudgetCreate
from auth import get_current_user

router = APIRouter()

# Income Routes
income_router = APIRouter(prefix="/income", tags=["Income"])

@income_router.post("/add")
def add_income(income: IncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_income = Income(user_id=current_user.id, amount=income.amount, date=income.date)
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
    new_expense = Expense(user_id=current_user.id, amount=expense.amount, date=expense.date)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@expense_router.get("/all")
def get_all_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Expense).filter(Expense.user_id == current_user.id).all()

# Budget Routes
budget_router = APIRouter(prefix="/budget", tags=["Budget"])

@budget_router.post("/add")
def add_budget(budget: BudgetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_budget = Budget(user_id=current_user.id, amount=budget.amount, date=budget.date,category=budget.category)
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

@budget_router.get("/all")
def get_all_budgets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Budget).filter(Budget.user_id == current_user.id).all()


@budget_router.delete("/delete/{id:int}")
def delete_budget(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget_to_delete = db.query(Budget).filter(Budget.id == id and Budget.user_id == current_user.id).first()
    if not budget_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget Not Found")
    db.delete(budget_to_delete)
    db.commit()
    return {"message": "Budget deleted successfully"}

@budget_router.put("/update/{id:int}")
def update_budget(id: int, budget: BudgetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    budget_to_update = db.query(Budget).filter(Budget.id == id, Budget.user_id == current_user.id).first()
    
    if not budget_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found or doesn't belong to the current user")
    
    
    if budget.amount:
        budget_to_update.amount = budget.amount
    if budget.date:
        budget_to_update.date = budget.date
    if budget.category:
        budget_to_update.category = budget.category
    
    
    db.commit()
    db.refresh(budget_to_update)
    
    return budget_to_update

# Include Routers
router.include_router(income_router)
router.include_router(expense_router)
router.include_router(budget_router)
