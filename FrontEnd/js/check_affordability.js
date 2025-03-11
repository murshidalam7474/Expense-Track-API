const API_URL = "http://127.0.0.1:8000/afford/can_afford/"; 
const token = localStorage.getItem("access_token"); 

async function checkAffordability() {
    const months = document.getElementById("monthsInput").value;
    const plannedExpense = document.getElementById("plannedExpenseInput").value;

    if (!months || months <= 0 || !plannedExpense || plannedExpense <= 0) {
        alert("Please enter valid values for months and planned expense.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}${months}/${plannedExpense}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch affordability data");
        }

        const data = await response.json();
        displayAffordability(data);
    } catch (error) {
        console.error("Error fetching affordability data:", error);
        alert("Error checking affordability.");
    }
}

function displayAffordability(data) {
    document.getElementById("isInDebt").textContent = data.is_in_debt;
    document.getElementById("advice").textContent = data.advice;
    document.getElementById("totalIncome").textContent = data.total_income;
    document.getElementById("totalExpenses").textContent = data.total_expenses;
    document.getElementById("totalBudget").textContent = data.total_budget;
    document.getElementById("netSavings").textContent = data.net_savings;
    document.getElementById("remainingAfterExpense").textContent = data.remaining_after_expense;
    document.getElementById("estimatedMonths").textContent = data.estimated_months_to_save;
    document.getElementById("suggestedSavings").textContent = data.suggested_savings_plan;
}
