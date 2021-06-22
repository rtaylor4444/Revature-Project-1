//DOM Objects
const dashPos = document.getElementById("navbar_container");
const username = localStorage.getItem("username");
if (username) {
    role = localStorage.getItem("user_role")
    console.log(role)
    if ((role & 2) == 0) {
        dashPos.innerHTML = `
        <nav class="navbar">
            <a id="dashboard_option" class="navbar__item" href="dashboard.html">Dashboard</a>
            <a id="logout_option" class="navbar__item navbar__item--right">Logout</a>
        </nav>
        `
    } else {
        dashPos.innerHTML = `
        <nav class="navbar">
            <a id="manage_option" class="navbar__item" href="manage.html">Manage</a>
            <a id="stats_option" class="navbar__item" href="stats.html">Statistics</a>
            <a id="logout_option" class="navbar__item navbar__item--right">Logout</a>
            <a class="navbar__item navbar__item--right" href="new_user.html">Register User</a>
        </nav>
        `
    }

    logoutOption = document.getElementById("logout_option")
    logoutOption.addEventListener('click', logout);
} else {
    window.location.href = `login.html`
}

async function logout() {
    const response = await fetch(`http://127.0.0.1:5000/users/logout`, {
        method: 'POST',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'username': localStorage.getItem("username")
        },
        referrerPolicy: 'no-referrer',
    });
    if (response.ok) {
        localStorage.removeItem("user_role");
        localStorage.removeItem("username");
        localStorage.removeItem("user_id");
        localStorage.removeItem("cur_reim");
        window.location.href = `login.html`;
    }
    else
        console.log(response.status)
}