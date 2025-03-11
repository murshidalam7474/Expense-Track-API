document.getElementById("incomeForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent default form submission

    const amount = document.getElementById("amount").value;
    const date = document.getElementById("date").value;
    const category = document.getElementById("category").value;

    if (!category) {
        alert("Category cannot be empty!");
        return;
    }

    const incomeData = {
        amount: parseFloat(amount),
        date: date,
        category: category
    };

    try {
        const token = localStorage.getItem("access_token"); // Assuming JWT is stored in local storage
        const response = await fetch("http://127.0.0.1:8000/income/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(incomeData)
        });

        if (response.ok) {
            alert("Income added successfully!");
            document.getElementById("incomeForm").reset();
        } else {
            const errorData = await response.json();
            alert("Failed to add income: " + (errorData.detail || "Unknown error"));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error adding income. Please try again.");
    }
});
