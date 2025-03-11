document.getElementById("addUserForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!name || !email || !password) {
        showMessage("All fields are required!", "error");
        return;
    } else if (!emailPattern.test(email)) {
        showMessage("Invalid email format. Please enter a valid email.", "error");
        return;
    }

    fetch("/create_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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
    .catch(error => showMessage("Failed to add user!", "error"));
});

function updateUser(userId) {
    let row = document.querySelector(`tr[data-id='${userId}']`);
    let name = row.querySelector(".edit-name").value.trim();
    let email = row.querySelector(".edit-email").value.trim();

    if (!name || !email) {
        showMessage("Name and email cannot be empty!", "error");
        return;
    }

    fetch(`/update_user/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, "error");
        } else {
            showMessage("User updated successfully!", "success");
            highlightRow(userId);
        }
    })
    .catch(error => showMessage("Failed to update user!", "error"));
}

function deleteUser(userId) {
    if (!confirm("Are you sure you want to delete this user?")) return;

    fetch(`/delete_user/${userId}`, { method: "DELETE" })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, "error");
        } else {
            showMessage("User deleted successfully!", "success");
            document.querySelector(`tr[data-id='${userId}']`).remove();
        }
    })
    .catch(error => showMessage("Failed to delete user!", "error"));
}

function showMessage(message, type) {
    let messageBox = document.getElementById("messageBox");
    messageBox.textContent = message;
    messageBox.className = type;
    messageBox.style.display = "block";

    // Ensure the message is visible for longer
    setTimeout(() => {
        messageBox.style.opacity = "1";
        messageBox.style.transition = "opacity 0.5s ease-in-out";
    }, 100);

    setTimeout(() => {
        messageBox.style.opacity = "0";
        setTimeout(() => messageBox.style.display = "none", 500);
    }, 3000);
}

function highlightRow(userId) {
    let row = document.querySelector(`tr[data-id='${userId}']`);
    row.style.backgroundColor = "#d4edda";
    setTimeout(() => row.style.backgroundColor = "", 1500);
}
