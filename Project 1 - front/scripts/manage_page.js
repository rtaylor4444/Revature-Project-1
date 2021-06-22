//Magic Trie Tree!!
class TrieNode {
    constructor() {
        this.children = new Map();
        this.index = -1;
    }
};
class Trie {
    constructor() {
        this.root = new TrieNode();
        this.curNode = this.root;
        this.size = 0;
    }

    addWord(word, index) {
        this.curNode = this.root;
        for (let i = 0; i < word.length; ++i) {
            if (!this.curNode.children.has(word[i]))
                this.curNode.children.set(word[i], new TrieNode())
            this.curNode = this.curNode.children.get(word[i]);
        }
        this.curNode.index = index;
        this.size++;
    }

    //-1 doesnt exist
    //0 partial word
    //1 complete word
    findWord(word) {
        this.curNode = this.root;
        for (let i = 0; i < word.length; ++i) {
            if (!this.curNode.children.has(word[i]))
                return -1;
            this.curNode = this.curNode.children.get(word[i]);
        }
        return this.curNode.index >= 0 ? 1 : 0;
    }

    getCurIndex() {
        return this.curNode.index;
    }
    getAllPossibleIndex() {
        let indexList = [];
        function recursive(curNode) {
            //Short-curciut if list size is 3
            if (indexList.length >= 3) return;
            if (curNode.index > -1) indexList.push(curNode.index);
            curNode.children.forEach(recursive);
        }
        recursive(this.curNode);
        return indexList;
    }
}

//DOM Objects
const pendReqContainer = document.getElementById("pend_req_container");
const allReqContainer = document.getElementById("all_req_container");
const allReimSearch = document.getElementById("all_reim_search");
allReimSearch.addEventListener("input", updateAllReimQuery);
const pendReimSearch = document.getElementById("pend_reim_search");
pendReimSearch.addEventListener("input", updatePendReimQuery);

//Globals
let allReqTrie = new Trie();
let pendReqTrie = new Trie();
let prevPendSearchString = "";
let idToResponse = new Map();
let pendingReims;
let allReims;

//Helper Functions
function getReimInnerHtml(reim, dom_id) {
    textColor = "u-color-yellow";
    statusText = "Pending";
    if (reim.status > 0) {
        textColor = "u-color-green";
        statusText = "Approved";
    }
    else if (reim.status < 0) {
        textColor = "u-color-red";
        statusText = "Denied";
    }

    return `
    <div id="${dom_id}">
        <h2 class="u-margin-bottom-small">Request #${reim.id}</h2>
        <h3>Amount: ${reim.amount}</h3>
        <p>${reim.reason}</p>
        <p class="${textColor}">${statusText}</p>
        <p class="u-margin-bottom-small">${reim.response}</p>
    </div>
    `;
}
function getPendReimInnerHtml(reim, dom_id) {
    return `
    <div id="pend_reim_child_${dom_id}">
        <h2 class="u-margin-bottom-small">Request #${reim.id}</h2>
        <h3>Amount: ${reim.amount}</h3>
        <p>${reim.reason}</p>
        <textarea id="reim_reason_${dom_id}" class="form__textarea" oninput="setResponse(${dom_id})"></textarea>
        <div class="row">
            <div class="col-1-of-2 u-center-text">
                <button id="cur_reim_deny_btn_${dom_id}" type="button" onclick="updatePendingReim(${dom_id}, -1)" 
                class="btn btn--red_small">Deny</button>
            </div>
            <div class="col-1-of-2 u-center-text">
                <button id="cur_reim_approve_btn_${dom_id}" type="button" onclick="updatePendingReim(${dom_id}, 1)" 
                class="btn btn--green_small">Approve</button>
            </div>
        </div>
    </div>
    `;
}
function getAllReimInnerHtml(reimRequests, reimHtmlFunc, dom_id) {
    let finalInnerHTML = ``;
    let numDisplay = 0;
    for (let i = 0; i < reimRequests.length; ++i) {
        //Limit Display to 3 previous requests
        if (numDisplay >= 3) break;
        finalInnerHTML += reimHtmlFunc(reimRequests[i], dom_id + i);
        ++numDisplay;
    }
    return finalInnerHTML;
}
function setDefaultDisplay(containerDOM, reimList, func, dom_id) {
    let finalInnerHTML = getAllReimInnerHtml(reimList, func, dom_id)
    if (finalInnerHTML !== "")
        containerDOM.innerHTML = finalInnerHTML;
    else
        containerDOM.innerHTML = `<h3>There are no requests</h3>`
}
function updateQuery(stringID, reimRequests, domID, trie, reimSearchDOM, reimContainerDOM, getReimFunc) {
    //Empty Search Query
    prevPendSearchString = stringID;
    if (stringID === "") {
        setDefaultDisplay(reimContainerDOM, reimRequests, getReimFunc, domID);
        return;
    }
    let searchResult = trie.findWord(stringID);
    //Successful + Partial Trie search
    if (searchResult >= 0) {
        let finalInnerHTML = "";
        let indices = trie.getAllPossibleIndex();
        for (let i = 0; i < indices.length; ++i) {
            finalInnerHTML += getReimFunc(reimRequests[indices[i]], domID + indices[i]);
        }
        reimContainerDOM.innerHTML = finalInnerHTML;
        if (searchResult === 1) reimSearchDOM.className = "form__input form__input--found"
        else reimSearchDOM.className = "form__input";
    }
    //Failed Trie search
    else {
        reimContainerDOM.innerHTML = `<h3>No requests match your search query</h3>`;
        reimSearchDOM.className = "form__input form__input--invalid"
    }
}
function updateAllReimQuery(e) {
    updateQuery(`${e.target.value}`, allReims, "all_reim_child_", allReqTrie, allReimSearch, allReqContainer, getReimInnerHtml);
}
function updatePendReimQuery(e) {
    updateQuery(`${e.target.value}`, pendingReims, "", pendReqTrie, pendReimSearch, pendReqContainer, getPendReimInnerHtml);
}
function setResponse(id) {
    let value = document.getElementById("reim_reason_" + id).value;
    idToResponse.set(id, value);
}
//API Calls
async function getAllPendingReim() {
    const response = await fetch(`http://127.0.0.1:5000/reimbursements/pending`, {
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
        pendingReims = await response.json();
        for (let i = 0; i < pendingReims.length; ++i)
            pendReqTrie.addWord(`${pendingReims[i].id}`, i);

        setDefaultDisplay(pendReqContainer, pendingReims, getPendReimInnerHtml, "");
    }
}
async function getAllReim() {
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
        allReims = await response.json();
        for (let i = 0; i < allReims.length; ++i)
            allReqTrie.addWord(`${allReims[i].id}`, i);

        setDefaultDisplay(allReqContainer, allReims, getReimInnerHtml, "all_reim_child_");
    }
}
async function updatePendingReim(index, status) {
    reim = pendingReims[index];
    res = idToResponse.has(index) ? idToResponse.get(index) : "";
    const response = await fetch(`http://127.0.0.1:5000/reimbursements/update/${reim.id}`, {
        method: 'PUT',
        mode: 'cors',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'username': localStorage.getItem("username")
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify({
            'amount': reim.amount,
            'reason': reim.reason,
            'owner': reim.owner,
            'status': status,
            'response': res
        })
    });
    //Update our page
    if (response.ok) {
        pendingReims.splice(index, 1);
        idToResponse.set(index, "");
        //console.log("Update display", pendingReims);
        updateQuery(prevPendSearchString, pendingReims, "", pendReqTrie,
            pendReimSearch, pendReqContainer, getPendReimInnerHtml);
        //BUG - All reims also needs to be updated
    }
}

getAllPendingReim();
getAllReim();