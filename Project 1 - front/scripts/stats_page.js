//Globals
let isData = false;
let employeeReqMoney = []
let totalMoney = [['Denied', 0,], ['Pending', 0], ['Approved', 0]];
let avgMoney = [['Denied', 0], ['Pending', 0], ['Approved', 0]];
let minMoney = [['Denied', 999999], ['Pending', 9999999], ['Approved', 999999]];
let maxMoney = [['Denied', 0], ['Pending', 0], ['Approved', 0]];

//Helper functions
async function processData(allReims) {
    let idToIndex = new Map();
    for (let i = 0; i < allReims.length; ++i) {
        //Amount Data
        totalMoney[allReims[i].status + 1][1] += allReims[i].amount;
        avgMoney[allReims[i].status + 1][1] += allReims[i].amount;
        minMoney[allReims[i].status + 1][1] = Math.min(allReims[i].amount,
            minMoney[allReims[i].status + 1][1]);
        maxMoney[allReims[i].status + 1][1] = Math.max(allReims[i].amount,
            maxMoney[allReims[i].status + 1][1]);
        //User data
        if (!idToIndex.has(allReims[i].owner)) {
            user = await getUser(allReims[i].owner);
            idToIndex.set(allReims[i].owner, employeeReqMoney.length);
            employeeReqMoney.push([user.name, 0]);
        }
        else {
            employeeReqMoney[idToIndex.get(allReims[i].owner)][1] += allReims[i].amount;
        }
    }
    avgMoney[0][1] /= allReims.length;
    avgMoney[1][1] /= allReims.length;
    avgMoney[2][1] /= allReims.length;
}

//Api Calls
async function getData() {
    const response = await fetch(`http://127.0.0.1:5000/reimbursements`, {
        method: 'GET',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'username': localStorage.getItem("username")
        },
        referrerPolicy: 'no-referrer',
    });
    //Update our page
    if (response.ok) {
        const allReims = await response.json();
        if (allReims.length !== 0) {
            isData = true;
            await processData(allReims);
        }
    }
}
async function getUser(id) {
    const response = await fetch(`http://127.0.0.1:5000/users/${id}`, {
        method: 'GET',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'username': localStorage.getItem("username")
        },
        referrerPolicy: 'no-referrer',
    });
    return await response.json();
}


function drawChart() {

    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Employee');
    data.addColumn('number', 'Amount');
    data.addRows(employeeReqMoney);

    // Set chart options
    var options = {
        backgroundColor: 'transparent',
        'title': 'How Much Money Employees Spend',
        'width': 400,
        'height': 300
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('emp_money_container'));
    chart.draw(data, options);
}

function drawBar(rows, dom_id, title) {
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Status');
    data.addColumn('number', 'Amount');
    data.addRows(rows);

    // Set chart options
    var options = {
        backgroundColor: 'transparent',
        'title': title,
        'width': 400,
        'height': 300
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.BarChart(document.getElementById(dom_id));
    chart.draw(data, options);
}

function drawAvgBar() {
    drawBar(avgMoney, 'avg_money_container', "Average money requested")
}
function drawTotalBar() {
    drawBar(totalMoney, 'total_money_container', "Total money requested")
}
function drawMinBar() {
    drawBar(minMoney, 'min_money_container', "Minimum money requested")
}
function drawMaxBar() {
    drawBar(maxMoney, 'max_money_container', "Maximum money requested")
}
async function startProcess() {
    await getData();
    if (isData) {
        // Load the Visualization API and the corechart package.
        google.charts.load('current', { 'packages': ['corechart'] });

        // Set a callback to run when the Google Visualization API is loaded.   
        google.charts.setOnLoadCallback(drawChart);
        google.charts.setOnLoadCallback(drawAvgBar);
        google.charts.setOnLoadCallback(drawTotalBar);
        google.charts.setOnLoadCallback(drawMinBar);
        google.charts.setOnLoadCallback(drawMaxBar);
    }
}

//Process
startProcess()
