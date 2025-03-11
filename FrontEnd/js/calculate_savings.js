const API_URL = "http://127.0.0.1:8000/savings/"; // Update with your actual API URL
const token = localStorage.getItem("access_token"); // Assuming JWT is stored in local storage

async function calculateSavings() {
    const months = document.getElementById("monthsInput").value;
    
    if (!months || months <= 0) {
        alert("Please enter a valid number of months.");
        return;
    }

    try {
        const response = await fetch(API_URL + months, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch savings data");
        }

        const data = await response.json();
        displaySavings(data);
    } catch (error) {
        console.error("Error fetching savings data:", error);
        alert("Error calculating savings.");
    }
}

function displaySavings(data) {
    document.getElementById("totalIncome").textContent = data.total_income;
    document.getElementById("totalExpenses").textContent = data.total_expenses;
    document.getElementById("totalBudget").textContent = data.total_budget;
    document.getElementById("savings").textContent = data.savings;
    document.getElementById("message").textContent = data.Suggestion_Savings[0].message;
    document.getElementById("finalSuggestion").textContent = data.Suggestion_Savings[0].final_suggestion;
}
