document.addEventListener("DOMContentLoaded", async function() {
    const tableBody = document.getElementById("expense-budget-table");

    try {
        const response = await fetch("http://localhost:8000/comparison/expense_budget", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("access_token")  // Assuming user authentication
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }

        const data = await response.json();
        
        const expenses = data.expenses;
        const budgets = data.budgets;
        
        const budgetMap = {};

        budgets.forEach(budget => {
            budgetMap[budget.category] = budget.amount;
        });

        expenses.forEach(expense => {
            const budgetAmount = budgetMap[expense.category] || 0;
            const row = `<tr>
                            <td>${expense.month}</td>
                            <td>${expense.category}</td>
                            <td>${expense.amount}</td>
                            <td>${expense.date}</td>
                            <td>${budgetAmount}</td>
                        </tr>`;
            tableBody.innerHTML += row;
        });

    } catch (error) {
        tableBody.innerHTML = `<tr><td colspan="3" class="text-center text-danger">${error.message}</td></tr>`;
    }
});
