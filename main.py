from fastapi import FastAPI
from database import engine, Base
from routes import users, income, expenses, budget, savings,financial_afford,expense_vs_budget
from fastapi.middleware.cors import CORSMiddleware


# Initialize the database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(users.router)
app.include_router(income.router)
app.include_router(expenses.router)
app.include_router(budget.router)
app.include_router(savings.router)
app.include_router(financial_afford.router)
app.include_router(expense_vs_budget.router)


