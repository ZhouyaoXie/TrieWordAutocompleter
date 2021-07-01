global ALPHABET_SIZE, letter_map
ALPHABET_SIZE = 26
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
letter_map = dict(zip(ALPHABET, range(ALPHABET_SIZE)))

class TrieNode:
    
    def __init__(self, isEnd = False):
        self.isEnd = isEnd
        self.children = [None] * ALPHABET_SIZE
        self.num_children = 0

    def isEndNode(self):
        return self.isEnd
    
    def hasChild(self, char):
        return self.children[letter_map[char]] != None
    
    def addChild(self, char):
        self.children[letter_map[char]] = TrieNode()
        self.num_children += 1
        return self.children[letter_map[char]]
    
    def setEnd(self):
        self.isEnd = True
        
    def getChild(self, char):
        return self.children[letter_map[char]]

class Trie:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        rt = self.root
        for c in word:
            if rt.hasChild(c):
                rt = rt.getChild(c)
            else:
                rt = rt.addChild(c)
        rt.setEnd()
        
    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        rt = self.root
        for c in word:
            rt = rt.getChild(c)
            if rt is None:
                return False
        return rt.isEndNode()
    
    def existsStartWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        rt = self.root
        for c in prefix:
            rt = rt.getChild(c)
            if rt is None:
                return False
        return True

    def startsWith(self, prefix: str):
        if not self.existsStartWith(prefix):
            return []
        re = []
        rt = self.root
        for c in prefix:
            rt = rt.getChild(c)

        def backtrack(rt, path):
            # accept condition
            if rt.isEnd:
                re.append(path)
                if rt.num_children == 0:
                    return
            # reject condition
            if rt.num_children == 0:
                return 
            # build on partial solution
            for c in ALPHABET:
                if rt.hasChild(c):
                    backtrack(rt.getChild(c), path + c)

        backtrack(rt, prefix)
        return re

# for testing

# def main():
#     trie = Trie()
#     for w in ['blue', 'baloon', 'balcony', 'ballad','bloom']:
#         trie.insert(w)
#     print('result', trie.startsWith('b'))

# if __name__ == "__main__":
#     main()

