from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Income, Expense, Budget, User  
from database import get_db
from auth import get_current_user  

router=APIRouter(prefix="/afford", tags=["Affordability"])
@router.get("/can_afford/{months}/{planned_expense}")
def can_afford_expense(months: int, planned_expense: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30 * months)
    
    total_income = db.query(Income).filter(Income.user_id == current_user.id, Income.date >= start_date).all()
    total_expense = db.query(Expense).filter(Expense.user_id == current_user.id, Expense.date >= start_date).all()
    total_budget = db.query(Budget).filter(Budget.user_id == current_user.id, Budget.date >= start_date).all()
    if not total_income and not total_expense:
        raise HTTPException(status_code=404, detail="No financial records found.")
    
    if not total_budget:
        raise HTTPException(status_code=404, detail="No budget records found.")
    
    income_sum = sum(i.amount for i in total_income)
    expense_sum = sum(e.amount for e in total_expense)
    budget_sum = sum(b.amount for b in total_budget)
    
    net_savings = income_sum - expense_sum
    
    
    
    if net_savings <=0:
        is_in_debt="you are in debt "
    else:
        is_in_debt="you are not in debt "

    # is_in_debt = net_savings < 0
    
    budget_amounts = {}
    for b in total_budget or []:
        print(b.category,"--->",b.amount)
        budget_amounts[b.category.lower()] = b.amount
    print("budget amounts:",budget_amounts)

    budget_deficits = {}
    category_min_expenses = {}
    
    for expense in total_expense:
        category = expense.category.lower()
        budget_amount = budget_amounts.get(category, 0)
        print(f"{expense.category}: {expense.amount}, Budgeted amount: {budget_amount}")
        if expense.amount > budget_amount:
            budget_deficits[category] = expense.amount - budget_amount
            print(f"{expense.category} is over budget by {expense.amount - budget_amount}")
        
        if category in category_min_expenses:
            category_min_expenses[category] = min(category_min_expenses[category], expense.amount)
            print(f"Updated minimum expense for {category}: {category_min_expenses[category]}")
        else:
            category_min_expenses[category] = expense.amount
            print(f"Added new minimum expense for {category}: {expense.amount}")
    
    remaining_deficit = sum(budget_deficits.values())
    
    affordability = net_savings - planned_expense
    advice = "You can afford this expense!" if affordability >= 0 else "You need to save more."
    
    
    if net_savings > 0:
        months_needed = planned_expense / net_savings
    else:
        months_needed = float('inf')  
    saving_recommendations = {
        "is_in_debt": is_in_debt,
        "advice": advice,
        "total_income": income_sum,
        "total_expenses": expense_sum,
        "total_budget": budget_sum,
        "net_savings": net_savings,
        "planned_expense": planned_expense,
        "remaining_after_expense": affordability,
        "over_budget_categories": [{"Category": cat, "Over budget by": amt} for cat, amt in budget_deficits.items()],
        "minimum_expenses_per_category": [{"Category": cat, "Minimum Amount Spent": amt} for cat, amt in category_min_expenses.items()],
        "suggested_savings_plan": f"Consider reducing expenses in {', '.join(budget_deficits.keys())} over the next few months. As per your data."
        if net_savings < planned_expense else "NA",
        "estimated_months_to_save": round(months_needed,2) if months_needed != float('inf') else "Saving required first"
    }
    
    return saving_recommendations
