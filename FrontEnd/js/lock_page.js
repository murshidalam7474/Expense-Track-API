document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.replace("login.html");
    } else {
       
        const payload = JSON.parse(atob(token.split(".")[1]));
        const username = payload.sub;

       
        document.getElementById("username").textContent = username;
    }
});
