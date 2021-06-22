//DOM Objects
const reimError = document.getElementById("reim_error");
const reimAmountError = document.getElementById("reim_amount_error");
const amountInput = document.getElementById("reim_amount");
const reimReasonError = document.getElementById("reim_reason_error");
const reasonInput = document.getElementById("reim_reason");
const submitButton = document.getElementById("reim_button");

//Global Variables
let numAmount = 0;
let reasonText = "";

//Helper Functions
function initializeFields() {
    if (!localStorage.getItem("cur_reim"))
        return;

    const reim = JSON.parse(localStorage.getItem("cur_reim"))
    numAmount = reim.amount;
    reasonText = reim.reason;
    console.log(reim);
    amountInput.value = reim.amount;
    reasonInput.value = reim.reason;
}
function verifyAmount() {
    return !(numAmount < 100 || numAmount > 10000)
}
function verifyReason() {
    return !(reasonText.length < 30 || reasonText.length > 200)
}
function enableButton() {
    if (verifyAmount() && verifyReason())
        submitButton.disabled = false;
    else
        submitButton.disabled = true;
}
async function postNewReim() {
    let response = await fetch(`http://127.0.0.1:5000/reimbursements/new`, {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'username': localStorage.getItem("username")
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({
            'amount': numAmount,
            'reason': reasonText,
            'owner': localStorage.getItem("user_id")
        })
    });
    return response;
}
async function updateCurReim() {
    let response = await fetch(`http://127.0.0.1:5000/reimbursements/update/me`, {
        method: 'PUT',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'username': localStorage.getItem("username")
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({
            'amount': numAmount,
            'reason': reasonText,
            'owner': localStorage.getItem("user_id")
        })
    });
    return response;
}
//Event Callbacks
amountInput.addEventListener('input', updateAmount);
function updateAmount(e) {
    numAmount = e.target.value;
    if (!verifyAmount()) {
        reimAmountError.innerText = "Amount must be between 100 and 10000 dollars";
        amountInput.className = "form__input form__input--invalid";
    } else {
        reimAmountError.innerText = ""
        amountInput.className = "form__input "
    }
    enableButton();
}

reasonInput.addEventListener('input', updateReason);
function updateReason(e) {
    reasonText = e.target.value;
    if (!verifyReason()) {
        reimReasonError.innerText = "Reason must be between 30 and 200 characters";
        reasonInput.className = "form__input form__input--invalid";
    } else {
        reimReasonError.innerText = ""
        reasonInput.className = "form__input "
    }
    enableButton();
}

//API Calls
async function submitReim() {
    const response = localStorage.getItem("cur_reim") ? await updateCurReim() : await postNewReim();
    if (!response.ok)
        reimError.innerText = await response.text();
    else {
        reimError.innerText = "";
        const reim = await response.json();
        localStorage.setItem("cur_reim", JSON.stringify(reim))
        window.location.href = `dashboard.html`
    }
}

//Process
initializeFields();