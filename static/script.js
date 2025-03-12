document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("jwt_token");
    const authButton = document.getElementById("authButton");

    const currentPath = window.location.pathname;

    if (!token && currentPath !== "/" && currentPath !== "/admin_login") {
        window.location.href = "/admin_login";
    }

    if (token) {
        authButton.textContent = "Admin Logout";
        authButton.onclick = logout;
    } else {
        authButton.textContent = "Admin Login";
        authButton.onclick = () => window.location.href = "/admin_login";
    }
});

document.getElementById("loginForm")?.addEventListener("submit", function (event) {
    event.preventDefault();

    let email = document.getElementById("loginEmail").value.trim();
    let password = document.getElementById("loginPassword").value.trim();

    fetch("/admin_login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("jwt_token", data.access_token);
            showMessage("Login successful!", "success");
            setTimeout(() => window.location.href = "/", 1000);
        } else {
            showMessage("Invalid username or password!", "error");
        }
    })
    .catch(() => showMessage("Failed to login!", "error"));
});

// 🔓 Logout Function
function logout() {
    localStorage.removeItem("jwt_token");
    window.location.href = "/";
}

// 🛠 Handle User Actions (Only for Admin)
document.getElementById("addUserForm")?.addEventListener("submit", function (event) {
    event.preventDefault();

    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let token = localStorage.getItem("jwt_token");

    if (!token) {
        showMessage("Unauthorized! Please log in.", "error");
        return;
    }

    fetch("/create_user", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name, email, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, "error");
        } else {
            showMessage("User added successfully!", "success");
            setTimeout(() => location.reload(), 1000);
        }
    })
    .catch(() => showMessage("Failed to add user!", "error"));
});

function updateUser(userId) {
    let row = document.querySelector(`tr[data-id='${userId}']`);
    let name = row.querySelector(".edit-name").value.trim();
    let email = row.querySelector(".edit-email").value.trim();
    let token = localStorage.getItem("jwt_token");

    if (!token) {
        showMessage("Unauthorized! Please log in.", "error");
        return;
    }

    fetch(`/update_user/${userId}`, {
        method: "PUT",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name, email }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, "error");
        } else {
            showMessage("User updated successfully!", "success");
            highlightRow(userId);
            setTimeout(() => location.reload(), 1000);
        }
    })
    .catch(() => showMessage("Failed to update user!", "error"));
}

function deleteUser(userId) {
    if (!confirm("Are you sure you want to delete this user?")) return;

    let token = localStorage.getItem("jwt_token");

    if (!token) {
        showMessage("Unauthorized! Please log in.", "error");
        return;
    }

    fetch(`/delete_user/${userId}`, {
        method: "DELETE",
        headers: { 
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, "error");
        } else {
            showMessage("User deleted successfully!", "success");
            document.querySelector(`tr[data-id='${userId}']`).remove();
        }
    })
    .catch(() => showMessage("Failed to delete user!", "error"));
}

// 🔔 Display Messages
function showMessage(message, type) {
    let messageBox = document.getElementById("messageBox");
    messageBox.textContent = message;
    messageBox.className = type;
    messageBox.style.display = "block";

    setTimeout(() => {
        messageBox.style.opacity = "1";
        messageBox.style.transition = "opacity 0.5s ease-in-out";
    }, 100);

    setTimeout(() => {
        messageBox.style.opacity = "0";
        setTimeout(() => messageBox.style.display = "none", 500);
    }, 3000);
}

// ✨ Highlight Updated Row
function highlightRow(userId) {
    let row = document.querySelector(`tr[data-id='${userId}']`);
    row.style.backgroundColor = "#d4edda";
    setTimeout(() => row.style.backgroundColor = "", 1500);
}
