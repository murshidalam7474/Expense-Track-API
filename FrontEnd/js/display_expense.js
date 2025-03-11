const API_URL = "http://127.0.0.1:8000/expenses/all"; // Update with your actual API URL
const token = localStorage.getItem("access_token"); // Assuming JWT is stored in local storage

// Fetch all expenses from API
async function fetchExpenses() {
    try {
        const response = await fetch(API_URL, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch expenses");
        }

        const expenses = await response.json();
        displayExpenses(expenses);
    } catch (error) {
        console.error("Error fetching expenses:", error);
        alert("Error loading expenses.");
    }
}

// Display expenses in the table
function displayExpenses(expenses) {
    const tableBody = document.getElementById("expenseTableBody");
    tableBody.innerHTML = ""; // Clear existing data

    expenses.forEach((expense) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            
            <td>${expense.amount}</td>
            <td>${expense.date}</td>
            <td>${expense.category}</td>
        `;

        tableBody.appendChild(row);
    });
}

// Fetch and display expenses on page load
fetchExpenses();
