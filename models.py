from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime,Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email=Column(String, unique=True, index=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)  # New field
    incomes = relationship("Income", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")

class Income(Base):
    __tablename__ = "income"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=False)  
    user = relationship("User", back_populates="incomes")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=False)  
    user = relationship("User", back_populates="expenses")

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=False)  
    user = relationship("User", back_populates="budgets")
