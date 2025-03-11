const API_URL = "http://127.0.0.1:8000"; // Change to your FastAPI base URL
const token = localStorage.getItem("access_token"); // Assuming JWT token is stored in local storage

// Fetch and display income list
async function fetchIncomeList() {
    try {
        const response = await fetch(`${API_URL}/income/all`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const incomes = await response.json();
        const tableBody = document.getElementById("incomeTableBody");
        tableBody.innerHTML = ""; // Clear previous data

        incomes.forEach(income => {
            const row = document.createElement("tr");
            row.innerHTML = `
                
                <td>${income.amount}</td>
                <td>${income.date}</td>
                <td>${income.category}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="openUpdateModal(${income.amount}, '${income.date}', '${income.category}')">
                        Update
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteIncome(${income.id})">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching incomes:", error);
    }
}

// Open modal and fill in the form
function openUpdateModal(id, amount, date, category) {
    document.getElementById("updateIncomeId").value = id;
    document.getElementById("updateAmount").value = amount;
    document.getElementById("updateDate").value = date;
    document.getElementById("updateCategory").value = category;

    var updateModal = new bootstrap.Modal(document.getElementById("updateModal"));
    updateModal.show();
}

// Update income
async function updateIncome() {
    const incomeId = document.getElementById("updateIncomeId").value;
    const incomeAmount = document.getElementById("updateAmount").value;
    const incomeDate = document.getElementById("updateDate").value;
    const incomeCategory = document.getElementById("updateCategory").value;

    const requestBody = {
        amount: incomeAmount ? parseFloat(incomeAmount) : undefined,
        date: incomeDate || undefined,
        category: incomeCategory || undefined
    };

    try {
        const response = await fetch(`${API_URL}/income/update/${incomeId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();
        if (response.ok) {
            alert("Income updated successfully!");
            var updateModal = bootstrap.Modal.getInstance(document.getElementById("updateModal"));
            updateModal.hide();
            fetchIncomeList(); // Refresh the table
        } else {
            alert(result.detail || "Error updating income.");
        }
    } catch (error) {
        console.error("Error updating income:", error);
        alert("Failed to update income.");
    }
}

// Delete income
async function deleteIncome(id) {
    if (!confirm("Are you sure you want to delete this income?")) return;

    try {
        const response = await fetch(`${API_URL}/income/delete/${id}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const result = await response.json();
        if (response.ok) {
            alert("Income deleted successfully!");
            fetchIncomeList(); // Refresh the table
        } else {
            alert(result.detail || "Error deleting income.");
        }
    } catch (error) {
        console.error("Error deleting income:", error);
        alert("Failed to delete income.");
    }
}

// Fetch income list on page load
fetchIncomeList();
