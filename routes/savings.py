from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session
from database import get_db
from models import Income, Expense, Budget, User
from schemas import IncomeCreate, ExpenseCreate, BudgetCreate
from auth import get_current_user
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

router = APIRouter()


# router = APIRouter()

# @router.get("/savings/{months}")
# def calculate_savings(months: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     end_date = datetime.utcnow()
#     start_date = end_date - timedelta(days=30 * months)
    
#     total_income = db.query(Income).filter(Income.user_id == current_user.id, Income.date >= start_date).all()
#     total_expense = db.query(Expense).filter(Expense.user_id == current_user.id, Expense.date >= start_date).all()
#     total_budget = db.query(Budget).filter(Budget.user_id == current_user.id, Budget.date >= start_date).all()
#     if not total_income and not total_expense:
#         raise HTTPException(status_code=404, detail="No financial records found.")
    
#     if not total_budget:
#         raise HTTPException(status_code=404, detail="No budget records found.")
#     income_sum = sum(i.amount for i in total_income)
#     expense_sum = sum(e.amount for e in total_expense)
#     budget_sum = sum(b.amount for b in total_budget)
#     # print(total_expense)
#     # print(total_expense[0].amount)
    
#     budget_savings = {}
#     for b in total_budget:
#         budget_savings[b.category.lower()] = b.amount  
#     budget_deficits = {}  
#     saved_beyond_budget = {}  
    
#     for expense in total_expense:
#         category = expense.category.lower()
#         if category in budget_savings:
#             remaining_budget = budget_savings[category] - expense.amount
#             if remaining_budget >= 0:
#                 saved_beyond_budget[category] = remaining_budget
#                 budget_savings[category] = remaining_budget
#             else:
#                 budget_deficits[category] = abs(remaining_budget)
#                 budget_savings[category] = 0
    
    
#     total_saved = sum(budget_savings.values())
#     total_deficit = sum(budget_deficits.values())
#     remaining_deficit = max(total_deficit - total_saved, 0)
    
#     overspent_message = ""
#     for cat, amt in budget_deficits.items():
#         overspent_message += f"{cat} by {amt}, "
#     overspent_message = overspent_message.rstrip(', ')
    
#     saved_message = ""
#     for cat, amt in saved_beyond_budget.items():
#         saved_message += f"{cat} by {amt}, "
#     saved_message = saved_message.rstrip(', ')
#     if len(saved_message)==0:
#         saved_message="None"

#     bs=max(budget_sum-expense_sum,0)
    
#     suggestions = {
#         "message": f"You overspent in {overspent_message}. You saved in {saved_message}.Great you saved  {bs} more than your budget. Your Overall exceeded amount is {remaining_deficit}.",
#         "category_budget": [{"Category": i.category, "Budget Amount": i.amount} for i in total_budget],
#         "category_expense": [{"Category": j.category, "Spent Amount": j.amount} for j in total_expense],
#         "category_over_budget": [{"Category": cat, "Over budget by": amt} for cat, amt in budget_deficits.items()],
#         "category_savings": [{"Category": cat, "Saved amount": amt} for cat, amt in budget_savings.items() if amt > 0],
#         "final_suggestion": f"Please try to save in {', '.join(budget_deficits.keys())}."
#     }
    
#     return {
#         "total_income": income_sum,
#         "total_expenses": expense_sum,
#         "total_budget": budget_sum,
#         "savings": income_sum - expense_sum,
#         "Suggestion_Savings": [suggestions]
#     }

@router.get("/savings/{months}")
def calculate_savings(months: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30 * months)
    
    total_income = db.query(Income).filter(Income.user_id == current_user.id, Income.date >= start_date).all()
    total_expense = db.query(Expense).filter(Expense.user_id == current_user.id, Expense.date >= start_date).all()
    total_budget = db.query(Budget).filter(Budget.user_id == current_user.id, Budget.date >= start_date).all()
    
    if not total_income and not total_expense:
        raise HTTPException(status_code=404, detail="No financial records found.")
    
    income_sum = sum(i.amount for i in total_income)
    expense_sum = sum(e.amount for e in total_expense)
    budget_sum = sum(b.amount for b in total_budget)
    
    budget_savings = {}
    for b in total_budget:
        budget_savings[b.category.lower()] = b.amount 
    budget_deficits = {}
    saved_beyond_budget = {}
    
    for expense in total_expense:
        category = expense.category.lower()
        budget_amount = budget_savings.get(category, 0)
        remaining_budget = budget_amount - expense.amount
        
        if remaining_budget >= 0:
            saved_beyond_budget[category] = remaining_budget
            budget_savings[category] = remaining_budget
        else:
            budget_deficits[category] = abs(remaining_budget)
            budget_savings[category] = 0
    
    total_saved = sum(budget_savings.values())
    total_deficit = sum(budget_deficits.values())
    remaining_deficit = max(total_deficit - total_saved, 0)
    
    overspent_message = ""
    for cat, amt in budget_deficits.items():
        overspent_message += f"{cat} by {amt}, "
    overspent_message = overspent_message.rstrip(', ')
    
    saved_message = ""
    for cat, amt in saved_beyond_budget.items():
        saved_message += f"{cat} by {amt}, "
    saved_message = saved_message.rstrip(', ')
    if len(saved_message)==0:
        saved_message="None"
    
    bs = max(budget_sum - expense_sum, 0)
    
    final_suggestion = "Please try to save in " + ", ".join(budget_deficits.keys()) if budget_deficits else "No overspending detected."
    
    suggestions = {
        "message": f"You overspent in {overspent_message}. You saved in {saved_message}. Great, you saved {bs} more than your budget. Your overall exceeded amount is {remaining_deficit}.",
        "category_budget": [{"Category": i.category, "Budget Amount": i.amount} for i in total_budget],
        "category_expense": [{"Category": j.category, "Spent Amount": j.amount} for j in total_expense],
        "category_over_budget": [{"Category": cat, "Over budget by": amt} for cat, amt in budget_deficits.items()],
        "category_savings": [{"Category": cat, "Saved amount": amt} for cat, amt in budget_savings.items() if amt > 0],
        "final_suggestion": final_suggestion
    }
    
    return {
        "total_income": income_sum,
        "total_expenses": expense_sum,
        "total_budget": budget_sum,
        "savings": income_sum - expense_sum,
        "Suggestion_Savings": [suggestions]
    }



