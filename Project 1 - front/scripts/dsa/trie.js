class TrieNode {
    constructor() {
        this.children = new Map();
        this.isWord = false;
    }
};

class Trie {
    constructor() {
        this.root = new TrieNode();
        this.curNode = this.root;
        this.size = 0;
    }

    addWord(word) {
        this.curNode = this.root;
        for (let i = 0; i < word.length; ++i) {
            if (!this.curNode.children.has(word[i]))
                this.curNode.children.set(word[i], new TrieNode())
            this.curNode = this.curNode.children.get(word[i]);
        }
        this.curNode.isWord = true;
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
        return this.curNode.isWord ? 1 : 0;
    }

    getCurIndex() {
        return this.curNode.index;
    }
}