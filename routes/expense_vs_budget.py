from fastapi import APIRouter, Depends, HTTPException, status
from models import Expense, Budget
from database import get_db
from sqlalchemy.orm.session import Session
from sqlalchemy import extract
from auth import get_current_user

router = APIRouter(
    prefix="/comparison",
    tags=["Expenses_VS_Budgets"],
)

@router.get("/expense_budget")
def compare_expen_budget(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    # Fetch all expenses for the current user
    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()

    # Fetch all budgets for the current user
    budgets = db.query(Budget).filter(
        Budget.user_id == current_user.id
    ).all()

    if not expenses and not budgets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses or budgets found")

    # Group expenses by category and store their respective dates
    expense_data = {}
    for expense in expenses:
        month = expense.date.strftime("%Y-%m")  # Extract year-month
        category = expense.category

        if (month, category) not in expense_data:
            expense_data[(month, category)] = {
                "amount": expense.amount,
                "date": expense.date.strftime("%Y-%m-%d")
            }
        else:
            expense_data[(month, category)]["amount"] += expense.amount  # Sum expenses of the same category in the same month

    # Convert expense data to a structured response
    formatted_expenses = [
        {"month": month, "category": category, "amount": data["amount"], "date": data["date"]}
        for (month, category), data in expense_data.items()
    ]

    return {
        "expenses": formatted_expenses,
        "budgets": budgets
    }
