document.getElementById("budgetForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const amount = document.getElementById("amount").value;
    const date = document.getElementById("date").value;
    const category = document.getElementById("category").value;

    const budgetData = {
        amount: parseFloat(amount),
        date: date,
        category: category
    };

    try {
        const token = localStorage.getItem("access_token"); // Assuming JWT is stored in local storage
        const response = await fetch("http://127.0.0.1:8000/budget/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(budgetData)
        });

        if (response.ok) {
            alert("Budget added successfully!");
            document.getElementById("budgetForm").reset();
        } else {
            const errorData = await response.json();
            alert("Failed to add budget: " + (errorData.detail || "Unknown error"));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error adding budget. Please try again.");
    }
});
