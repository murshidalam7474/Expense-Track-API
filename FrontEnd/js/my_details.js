const API_URL = "http://127.0.0.1:8000/users/me"; // Update with your actual API URL
const token = localStorage.getItem("access_token"); // Assuming JWT is stored in local storage

// Fetch user details
async function fetchUserDetails() {
    try {
        const response = await fetch(API_URL, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch user details");
        }

        const userDetails = await response.json();
        displayUserDetails(userDetails);
    } catch (error) {
        console.error("Error fetching user details:", error);
        alert("Error loading user details.");
    }
}

// Display user details in the UI
function displayUserDetails(data) {
    document.getElementById("username").textContent = `Username: ${data.username}`;
    document.getElementById("totalIncome").textContent = data.total_income;
    document.getElementById("totalExpense").textContent = data.total_expense;
    document.getElementById("totalBudget").textContent = data.total_budget;
    document.getElementById("balance").textContent = data.balance;
}

// Fetch and display user details on page load
fetchUserDetails();
