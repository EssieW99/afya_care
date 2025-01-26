
const loginContainer = document.getElementById("login");
const registerContainer = document.getElementById("register");
const loginBtn = document.querySelector("#login .submit");
const registerSubmitBtn = document.querySelector("#register .submit");

function login() {
    loginContainer.style.left = "4px";
    registerContainer.style.right = "-520px";
    loginBtn.parentElement.parentElement.style.opacity = 1;
    registerContainer.style.opacity = 0;
}

function register() {
    loginContainer.style.left = "-510px";
    registerContainer.style.right = "5px";
    loginContainer.style.opacity = 0;
    registerContainer.style.opacity = 1;
}

loginBtn.addEventListener("click", async () => {
    const email = document.querySelector("#login #emailBtn").value.trim();
    const password = document.querySelector("#login #passwordBtn").value.trim();

    if (!email || !password) {
        alert("Please fill in all fields.");
        return;
    }

    const userData = {
        email: email,
        password: password
    };

    try {
        const response = await fetch("https://afya-care.onrender.com/api/v1/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData),
        });

        if (response.ok) {
            const result = await response.json();
            alert("Login successful!");
            window.location.href = result.redirect_url;

        } else {
            const error = await response.json();
            alert(error.message || "Login failed. Please try again.");
        }
    } catch (err) {
        console.error("Error during login:", err);
        alert("An error occurred. Please try again later.");
    }
});

registerSubmitBtn.addEventListener("click", async (event) => {
    event.preventDefault();

    const firstName = document.querySelector("#register input[placeholder='FirstName']").value;
    const lastName = document.querySelector("#register input[placeholder='LastName']").value;
    const email = document.querySelector("#register input[placeholder='Email']").value;
    const nationalId = document.querySelector("#register input[placeholder='NationalId']").value;
    const phoneNumber = document.querySelector("#register input[placeholder='PhoneNumber']").value;
    const password = document.querySelector("#register input[placeholder='Password']").value;

    if (!firstName || !lastName || !email || !nationalId || !phoneNumber || !password) {
        alert("Please fill in all fields.");
        return;
    }

    const userData = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        national_id: nationalId,
        phone_number: phoneNumber,
        password: password,
    };

    console.log("Payload sent to backend:", userData);
    try {
        const response = await fetch("https://afya-care.onrender.com/api/v1/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userData),
        });
    
        if (response.ok) {
            const result = await response.json();
            alert("Registration successful!");
            window.location.href = result.redirect_url;
            
        } else {
            const error = await response.json();
            alert(error.message || "Registration failed. Please try again.");

        }
    } catch (err) {
        console.error("Error during registration:", err);
        alert("An error occurred. Please try again later.");
    }
});