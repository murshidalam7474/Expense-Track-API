from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User,Income, Expense,Budget
from sqlalchemy.sql import func
from schemas import UserCreate, UserResponse, Token
from auth import get_password_hash, authenticate_user, create_access_token, get_current_user,ALGORITHM,SECRET_KEY
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from email_utils import send_verification_email
import jwt

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_user or existing_email:
        raise HTTPException(status_code=400, detail="Username or email already taken")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email,username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}




@router.get("/me", response_model=dict)
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    total_income = db.query(func.sum(Income.amount)).filter(Income.user_id == current_user.id).scalar() or 0

    
    total_expense = db.query(func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).scalar() or 0

   
    total_budget = db.query(func.sum(Budget.amount)).filter(Budget.user_id == current_user.id).scalar() or 0

   
    balance = total_income - total_expense

    return {
        
        "username": current_user.username,
        "email": current_user.email,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_budget": total_budget,
        "balance": balance
    }

