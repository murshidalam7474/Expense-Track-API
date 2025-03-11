const API_BASE_URL = "http://127.0.0.1:8000"; // Replace with your actual FastAPI URL
const token = localStorage.getItem("access_token"); // Assuming JWT token is stored in localStorage

document.addEventListener("DOMContentLoaded", function () {
    fetchBudgetCategories();
});

// Fetch budget categories from the backend
async function fetchBudgetCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/budget/all`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch categories");
        }

        const budgets = await response.json();
        const categorySelect = document.getElementById("category");

        budgets.forEach(budget => {
            const option = document.createElement("option");
            option.value = budget.category;
            option.textContent = budget.category;
            categorySelect.appendChild(option);
        });

        // Add "Other" option at the end
        const otherOption = document.createElement("option");
        otherOption.value = "other";
        otherOption.textContent = "Other";
        categorySelect.appendChild(otherOption);

        // Add event listener for "Other" category selection
        categorySelect.addEventListener("change", function () {
            const customCategoryDiv = document.getElementById("customCategoryDiv");
            if (this.value === "other") {
                customCategoryDiv.style.display = "block";
            } else {
                customCategoryDiv.style.display = "none";
            }
        });

    } catch (error) {
        console.error("Error fetching categories:", error);
    }
}

// Handle form submission
document.getElementById("expenseForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const amount = document.getElementById("amount").value;
    const date = document.getElementById("date").value;
    let category = document.getElementById("category").value;
    const customCategory = document.getElementById("customCategory").value;

    if (category === "other" && customCategory.trim() !== "") {
        category = customCategory; // Use the custom category
    } else if (category === "other") {
        alert("Please enter a category.");
        return;
    }

    const expenseData = {
        amount: parseFloat(amount),
        date: date,
        category: category
    };

    try {
        const response = await fetch(`${API_BASE_URL}/expenses/add`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(expenseData)
        });

        if (response.ok) {
            alert("Expense added successfully!");
            document.getElementById("expenseForm").reset();
            document.getElementById("customCategoryDiv").style.display = "none"; // Hide custom category field
        } else {
            const errorData = await response.json();
            alert("Failed to add expense: " + (errorData.detail || "Unknown error"));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error adding expense. Please try again.");
    }
});
