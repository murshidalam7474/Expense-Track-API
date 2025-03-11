const API_URL = "http://127.0.0.1:8000/budget"; 
const token = localStorage.getItem("access_token"); 

// Fetch budgets from API
async function fetchBudgets() {
    try {
        const response = await fetch(`${API_URL}/all`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch budgets");
        }

        const budgets = await response.json();
        displayBudgets(budgets);
    } catch (error) {
        console.error("Error fetching budgets:", error);
        alert("Error loading budgets.");
    }
}

// Display budgets in the table
function displayBudgets(budgets) {
    const tableBody = document.getElementById("budgetTableBody");
    tableBody.innerHTML = ""; // Clear existing data

    budgets.forEach((budget) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            
            <td>${budget.amount}</td>
            <td>${budget.date}</td>
            <td>${budget.category}</td>
            <td>
                <button class="btn btn-warning btn-sm" onclick="openUpdateModal( ${budget.amount}, '${budget.date}', '${budget.category}')">
                    Update
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteBudget(${budget.id})">
                    Delete
                </button>
            </td>
        `;

        tableBody.appendChild(row);
    });
}

// Open Update Modal
function openUpdateModal(id, amount, date, category) {
    console.log("Opening modal for:", id, amount, date, category); // Debugging

    document.getElementById("updateBudgetId").value = id;
    document.getElementById("updateAmount").value = amount;
    document.getElementById("updateDate").value = date;
    document.getElementById("updateCategory").value = category;

    // Open Bootstrap modal properly
    let modalElement = document.getElementById("updateModal");
    if (!modalElement) {
        console.error("Update modal not found in DOM!");
        return;
    }

    let updateModal = new bootstrap.Modal(modalElement);
    updateModal.show();
}

// Update Budget
async function updateBudget() {
    const budgetId = document.getElementById("updateBudgetId").value;
    const budgetAmount = document.getElementById("updateAmount").value;
    const budgetDate = document.getElementById("updateDate").value;
    const budgetCategory = document.getElementById("updateCategory").value;

    const requestBody = {
        amount: budgetAmount ? parseFloat(budgetAmount) : undefined,
        date: budgetDate || undefined,
        category: budgetCategory || undefined
    };

    try {
        const response = await fetch(`${API_URL}/update/${budgetId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();
        if (response.ok) {
            alert("Budget updated successfully!");
            var updateModal = bootstrap.Modal.getInstance(document.getElementById("updateModal"));
            updateModal.hide();
            fetchBudgets(); // Refresh the table
        } else {
            alert(result.detail || "Error updating budget.");
        }
    } catch (error) {
        console.error("Error updating budget:", error);
        alert("Failed to update budget.");
    }
}

// Delete Budget
async function deleteBudget(id) {
    if (!confirm("Are you sure you want to delete this budget?")) return;

    try {
        const response = await fetch(`${API_URL}/delete/${id}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const result = await response.json();
        if (response.ok) {
            alert("Budget deleted successfully!");
            fetchBudgets(); // Refresh the table
        } else {
            alert(result.detail || "Error deleting budget.");
        }
    } catch (error) {
        console.error("Error deleting budget:", error);
        alert("Failed to delete budget.");
    }
}

// Fetch and display budgets on page load
fetchBudgets();
