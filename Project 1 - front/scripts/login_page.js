//Redirect if already logged in
if ((localStorage.getItem("role") & 1) !== 0)
    window.location.href = `dashboard.html`;
else if ((localStorage.getItem("role") & 2) !== 0)
    window.location.href = `manage.html`;

//DOM Objects
const loginError = document.getElementById("login_error");
const loginUsernameError = document.getElementById("login_username_error");
const usernameInput = document.getElementById("login_username");
const loginPasswordError = document.getElementById("login_password_error");
const passwordInput = document.getElementById("login_password");
const loginButton = document.getElementById("login_button");

//Global Variables
let usernameText = "";
let passwordText = "";

//Helper Functions
function verifyText(text) {
    return !(text.length < 3 || text.length > 50)
}
function updateErrorText(domError, domInput, name, text) {
    if (!verifyText(text)) {
        domError.innerText = name + " must be between 3 and 50 characters";
        domInput.className = "form__input form__input--invalid";
    } else {
        domError.innerText = ""
        domInput.className = "form__input "
    }
}
function enableButton() {
    if (verifyText(usernameText) && verifyText(passwordText))
        loginButton.disabled = false;
    else
        loginButton.disabled = true;
}

//Event Callbacks
usernameInput.addEventListener('input', updateUsername);
function updateUsername(e) {
    usernameText = e.target.value;
    updateErrorText(loginUsernameError, usernameInput, "Username", usernameText);
    enableButton();
}

passwordInput.addEventListener('input', updatePassword);
function updatePassword(e) {
    passwordText = e.target.value;
    updateErrorText(loginPasswordError, passwordInput, "Password", passwordText);
    enableButton();
}

//API Calls
async function submitLoginForm() {
    const response = await fetch(`http://127.0.0.1:5000/users/login`, {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({
            'username': usernameText,
            'password': passwordText
        })
    });

    if (!response.ok)
        loginError.innerText = await response.text();
    else {
        loginError.innerText = "";
        const user = await response.json();
        localStorage.setItem("user_role", user.role);
        localStorage.setItem("username", user.username);
        localStorage.setItem("user_id", user.id);
        if ((user.role & 2) !== 0)
            window.location.href = `manage.html`
        else
            window.location.href = `dashboard.html`
    }
}