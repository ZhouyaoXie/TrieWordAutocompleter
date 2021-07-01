from tkinter import Tk, ttk, font
from ttkthemes import ThemedTk
from TrieClass import Trie
import time
import sys
import pickle
import os

class App:
    def __init__(self, master):
        self.master = master
        master.title("Word Autocompleter")
        master.geometry("450x600")
        self.myFont = font.Font(family='TkHeadingFont', size=14)
        self.myTextFont = font.Font(family='TkTextFont', size=14)
        s = ttk.Style()
        #s.configure('My.TButton', font=('TkTextFont', 14))
        #s.configure('My.TLabel', font = ('TkTextFont', 14))
        s.configure('.', font = ('TkTextFont', 14))
        self.RUNNING = True
        self.display_rows = 15

        self.load_trie()

        self.label = ttk.Label(master, text="Enter word below", font = self.myFont)
        self.label.pack()

        vcmd = (master.register(self.validate_input))
        self.enter = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), font = self.myFont)
        self.enter.pack()
        
        self.results = []
        for i in range(self.display_rows):
            self.results.append(ttk.Label(master, text="", padding = 2.5, font = self.myTextFont))
            self.results[i].pack()

        self.close_button = ttk.Button(master, text="Close", command=self.quit, style = 'My.TButton')
        self.close_button.pack(side = "bottom")
        
        self.on()

    def load_trie(self):
        if 'corpus_trie.pickle' in os.listdir():
            with open('corpus_trie.pickle', 'rb') as f:
                self.corpus = pickle.load(f)
            f.close()
        else:
            self.corpus = Trie()
            with open('words_alpha.txt', 'r') as f:
                for word in f:
                    word = word.rstrip('\n')
                    self.corpus.insert(word)
            f.close()
            with open('corpus_trie.pickle', 'wb') as f:
                pickle.dump(self.corpus, f)
            f.close()

    def get_candidates(self, prefix):
        return self.corpus.startsWith(prefix)
        
    def quit(self):
        self.RUNNING = False
        self.master.destroy()
        
    def validate_input(self, s):
        if s == '':
            return True
        if s.isalpha():
            return True
        return False

    def update_words(self, prefix):
        if prefix == '':
            candidates = []
        else:
            candidates = self.get_candidates(prefix)
        for i in range(min(self.display_rows, len(candidates))):
            self.results[i].config(text = candidates[i])
        if len(candidates) < self.display_rows:
            for i in range(len(candidates),self.display_rows):
                self.results[i].config(text = '')
            
    def on(self):
        prev = self.enter.get()
        while self.RUNNING:
            time.sleep(0.01)
            self.master.update()
            try:
                val = self.enter.get()
                if val != prev:
                    self.update_words(val)
                    prev = val
            except:
                sys.exit(0)

root = ThemedTk(theme='breeze')
my_gui = App(root)
root.mainloop()