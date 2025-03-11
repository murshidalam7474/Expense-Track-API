document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const errorMessage = document.getElementById("error-message");

        errorMessage.textContent = ""; // Clear previous errors

        
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (password !== confirmPassword) {
            errorMessage.textContent = "Passwords do not match.";
            return;
        }

        // if (!passwordRegex.test(password)) {
        //     errorMessage.textContent = "Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, one number, and one special character.";
        //     return;
        // }

        const payload = {
            username,
            password
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/users/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                // alert("Signup successful! Redirecting to home page...");
                    window.location.href = "index.html";
               
            } else {
                errorMessage.textContent = data.detail || "Signup failed. Please try again.";
            }
        } catch (error) {
            errorMessage.textContent = "An error occurred. Please check your connection.";
        }
    });
});
// document.addEventListener("DOMContentLoaded", function () {
//     const signupForm = document.getElementById("signup-form");
//     const errorMessage = document.getElementById("error-message");

//     signupForm.addEventListener("submit", async function (event) {
//         event.preventDefault();

//         const username = document.getElementById("username").value.trim();
//         const email = document.getElementById("email").value.trim();
//         const password = document.getElementById("password").value;
//         const confirmPassword = document.getElementById("confirm-password").value;

//         errorMessage.textContent = ""; // Clear any previous errors

//         if (password !== confirmPassword) {
//             errorMessage.textContent = "Passwords do not match.";
//             return;
//         }

//         try {
//             const response = await fetch("http://127.0.0.1:8000/users/register", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify({
//                     username: username,
//                     email: email,
//                     password: password
//                 })
//             });

//             const data = await response.json();

//             if (response.ok) {
//                 alert("Registration successful! Please check your email for verification.");
//                 window.location.href = "login.html"; // Redirect to login page after successful registration
//             } else {
//                 errorMessage.textContent = data.detail || "An error occurred during registration.";
//             }
//         } catch (error) {
//             errorMessage.textContent = "An error occurred. Please check your connection.";
//         }
//     });
// });
