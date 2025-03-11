

document.getElementById("logout-btn").addEventListener("click", function () {
    localStorage.removeItem("access_token"); // Clear stored token
    alert("Logged out successfully!");
    window.location.href = "login.html"; // Redirect to login page
});

