async function registerUser() {
    const user_id = document.getElementById("user_id").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, password })
    });
    const result = await response.json();
    document.getElementById("registerMessage").textContent = result.message;
}

async function loginUser() {
    const user_id = document.getElementById("user_id").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, password })
    });
    const result = await response.json();
    document.getElementById("loginMessage").textContent = result.message;
}
