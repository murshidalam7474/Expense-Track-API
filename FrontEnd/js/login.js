document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const errorMessage = document.getElementById("error-message");

        errorMessage.textContent = ""; 

        try {
            const response = await fetch("http://127.0.0.1:8000/users/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
               
                localStorage.setItem("access_token", data.access_token);

                alert("Login successful! Redirecting to home page...");
                
                
                window.location.href = "index.html";
            } else {
                errorMessage.textContent = data.detail || "Invalid username or password.";
            }
        } catch (error) {
            errorMessage.textContent = "An error occurred. Please check your connection.";
        }
    });
});
// document.addEventListener("DOMContentLoaded", function () {
//     const loginForm = document.getElementById("login-form");
//     const resendButton = document.getElementById("resend-verification");
//     const errorMessage = document.getElementById("error-message");

//     loginForm.addEventListener("submit", async function (event) {
//         event.preventDefault();

//         const username = document.getElementById("username").value.trim();
//         const password = document.getElementById("password").value;
//         errorMessage.textContent = ""; // Clear any previous errors

//         try {
//             const response = await fetch("http://127.0.0.1:8000/users/login", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/x-www-form-urlencoded"
//                 },
//                 body: new URLSearchParams({ username, password })
//             });

//             const data = await response.json();

//             if (response.ok) {
//                 // ✅ Store token securely in localStorage
//                 localStorage.setItem("access_token", data.access_token);

//                 alert("Login successful! Redirecting to home page...");
                
//                 // Redirect to index.html
//                 window.location.href = "index.html";
//             } else {
//                 errorMessage.textContent = data.detail || "Invalid username or password.";
//             }
//         } catch (error) {
//             errorMessage.textContent = "An error occurred. Please check your connection.";
//         }
//     });

//     // Handle resend verification email
//     resendButton.addEventListener("click", async function () {
//         const email = document.getElementById("username").value.trim(); // Assuming username is the email

//         if (!email) {
//             errorMessage.textContent = "Please enter your email to resend the verification.";
//             return;
//         }

//         try {
//             const response = await fetch("http://127.0.0.1:8000/users/resend-verification", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify({ email })
//             });

//             const data = await response.json();

//             if (response.ok) {
//                 alert("Verification email resent successfully!");
//             } else {
//                 errorMessage.textContent = data.detail || "Failed to resend verification email.";
//             }
//         } catch (error) {
//             errorMessage.textContent = "An error occurred. Please try again.";
//         }
//     });
// });
