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

//Dom Objects
const allReimContainer = document.getElementById("prev_req_container");
const currentReimContainer = document.getElementById("curr_req_container");
const reimButtom = document.getElementById("pending_reim_button");
reimButtom.addEventListener("click", () => { window.location.href = `user_reim.html` });
const reimSearch = document.getElementById("reim_search");
reimSearch.addEventListener("input", updateQuery);

//Globals
let prevReqTrie = new Trie();
let curReimRequest = -1;
let allPrevReimRequests = -1;

//Helper Functions
function getReimbursementInnerHtml(reim, dom_id) {
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
function getAllPrevReimInnerHtml() {
    let finalInnerHTML = ``;
    let numDisplay = 0;
    for (let i = 0; i < allPrevReimRequests.length; ++i) {
        //Skip Pending requests
        if (allPrevReimRequests[i].status == 0) continue;
        //Limit Display to 3 previous requests
        if (numDisplay >= 3) break;
        finalInnerHTML += getReimbursementInnerHtml(allPrevReimRequests[i], "prev_req_child_" + i);
        ++numDisplay;
    }
    return finalInnerHTML;
}
function updateQuery(e) {
    let stringID = `${e.target.value}`;
    //Empty Search Query
    if (stringID === "") {
        let finalInnerHTML = getAllPrevReimInnerHtml();
        if (finalInnerHTML === "") allReimContainer.innerHTML = `<h3>You have no previous requests</h3>`
        else allReimContainer.innerHTML = finalInnerHTML;
        return;
    }
    let searchResult = prevReqTrie.findWord(stringID);
    //Successful + Partial Trie search
    if (searchResult >= 0) {
        let finalInnerHTML = "";
        let indices = prevReqTrie.getAllPossibleIndex();
        for (let i = 0; i < indices.length; ++i) {
            finalInnerHTML += getReimbursementInnerHtml(allPrevReimRequests[indices[i]], "prev_req_child_" + indices[i]);
        }
        allReimContainer.innerHTML = finalInnerHTML;
        if (searchResult === 1) reimSearch.className = "form__input form__input--found"
        else reimSearch.className = "form__input";
    }
    //Failed Trie search
    else {
        allReimContainer.innerHTML = `<h3>No previous requests match your search query</h3>`;
        reimSearch.className = "form__input form__input--invalid"
    }
}
//Process
//Get our current reimbursement request if we have one
async function getCurrentReim() {
    const response = await fetch(`http://127.0.0.1:5000/reimbursements/me`, {
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
        curReimRequest = await response.json();
        currentReimContainer.innerHTML = getReimbursementInnerHtml(curReimRequest, "cur_req_child_0")
        reimButtom.innerText = "Update Request"
    }
    else
        reimButtom.innerText = "New Request"

    reimButtom.disabled = false;
}

async function getAllReim() {
    //Get all of our previous requests
    response = await fetch(`http://127.0.0.1:5000//reimbursements/all`, {
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
        allPrevReimRequests = await response.json();
        //Exit if no previous requests
        if (allPrevReimRequests.length === 0)
            return;

        for (let i = 0; i < allPrevReimRequests.length; ++i) {
            if (allPrevReimRequests[i].status == 0) continue;
            //Place id and index inside of our Trie Tree
            prevReqTrie.addWord(`${allPrevReimRequests[i].id}`, i);
        }
        let finalInnerHTML = getAllPrevReimInnerHtml();
        if (finalInnerHTML !== "")
            allReimContainer.innerHTML = finalInnerHTML;
    }
}

//Process
getCurrentReim()
getAllReim()