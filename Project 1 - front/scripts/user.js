//Redirect if user is already logged in
if ((localStorage.getItem("user_role") & 1) !== 0)
    window.location.href = `dashboard.html`;

//DOM Objects
const formContainer = document.getElementById("form_container");
let submitButton, nameInput, usernameInput, passwordInput, statusInput;
let userError, nameError, usernameError, passwordError, statusError;

//Global Variables
let nameText = "";
let usernameText = "";
let passwordText = "";
let status = 1;

//Helper functions
function initializeForm() {
    if ((localStorage.getItem("user_role") & 2) !== 0) {
        formContainer.innerHTML = `
        <p id="user_error" class="form__label--invalid u-center-text"></p>
        <label class="form__label">Your Name</label>
        <input id="user_name" type="text" class="form__input " />
        <div id="user_name_error" class="form__label--invalid"></div>
        <label class="form__label">Username</label>
        <input id="user_username" type="text" class="form__input " />
        <div id="user_username_error" class="form__label--invalid"></div>
        <label class="form__label">Password</label>
        <input id="user_password" type="password" class="form__input " />
        <div id="user_password_error" class="form__label--invalid"></div>
        <label class="form__label">Status</label>
        <input id="user_status" type="number" class="form__input " />
        <div id="user_status_error" class="form__label--invalid"></div>
        <div class="u-center-text">
            <button id="user_button" onclick="submitUserForm()" type="button" disabled
            class="btn">Submit</button>
        </div>
        `
        statusError = document.getElementById("user_status_error");
        statusInput = document.getElementById("user_status");
        statusInput.addEventListener('input', updateStatus);
    }
    else {
        formContainer.innerHTML = `
        <p id="user_error" class="form__label--invalid u-center-text"></p>
        <label class="form__label">Your Name</label>
        <input id="user_name" type="text" class="form__input " />
        <div id="user_name_error" class="form__label--invalid"></div>
        <label class="form__label">Username</label>
        <input id="user_username" type="text" class="form__input " />
        <div id="user_username_error" class="form__label--invalid"></div>
        <label class="form__label">Password</label>
        <input id="user_password" type="password" class="form__input " />
        <div id="user_password_error" class="form__label--invalid"></div>
        <div class="u-center-text">
            <button id="user_button" onclick="submitUserForm()" type="button" disabled
            class="btn">Submit</button>
        </div>
        `;
    }
    submitButton = document.getElementById("user_button");
    userError = document.getElementById("user_error");
    nameError = document.getElementById("user_name_error");
    nameInput = document.getElementById("user_name");
    nameInput.addEventListener('input', updateName);
    usernameError = document.getElementById("user_username_error");
    usernameInput = document.getElementById("user_username");
    usernameInput.addEventListener('input', updateUsername);
    passwordError = document.getElementById("user_password_error");
    passwordInput = document.getElementById("user_password");
    passwordInput.addEventListener('input', updatePassword);

}
function verifyText(text) {
    return !(text.length < 3 || text.length > 50)
}
function verifyStatus() {
    return !(status < 1 || status > 3)
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
function updateStatusText() {
    if (!verifyStatus()) {
        statusError.innerText = "Status must be a number between 1 and 3";
        statusInput.className = "form__input form__input--invalid";
    } else {
        statusError.innerText = ""
        statusInput.className = "form__input "
    }
}
function enableButton() {
    const isTextVerify = verifyText(usernameText) &&
        verifyText(passwordText) && verifyText(nameText);
    const isStatusVerify = (localStorage.getItem("role") & 2) !== 0 ?
        verifyStatus() : true;
    if (isTextVerify && isStatusVerify)
        submitButton.disabled = false;
    else
        submitButton.disabled = true;
}

//Event Callbacks
function updateName(e) {
    nameText = e.target.value;
    updateErrorText(nameError, nameInput, "Your name", nameText);
    enableButton();
}
function updateUsername(e) {
    usernameText = e.target.value;
    updateErrorText(usernameError, usernameInput, "Username", usernameText);
    enableButton();
}
function updatePassword(e) {
    passwordText = e.target.value;
    updateErrorText(passwordError, passwordInput, "Password", passwordText);
    enableButton();
}
function updateStatus(e) {
    status = e.target.value;
    updateStatusText();
    enableButton();
}

//API Calls
async function submitUserForm() {
    const response = await fetch(`http://127.0.0.1:5000/users/new`, {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'username': localStorage.getItem("username")
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({
            'name': nameText,
            'username': usernameText,
            'password': passwordText,
            'role': status,
            'blackmark': false
        })
    });

    if (!response.ok)
        userError.innerText = await response.text();
    else {
        userError.innerText = "";
        if ((localStorage.getItem("user_role") & 2) !== 0) {
            //This new user will not be logged in
            window.location.href = `manage.html`
        } else {
            const user = await response.json();
            localStorage.setItem("user_role", user.role);
            localStorage.setItem("username", user.username);
            localStorage.setItem("user_id", user.id);
            window.location.href = `dashboard.html`
        }
    }
}

//Process
initializeForm();