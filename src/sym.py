import math


class SYM:
    def __init__(self, at = None, txt = None):
        """
        Constructor for SYM Class
        n : Count of symbols
        has : Dictionary with count
        most : Symbol with most number of entries
        mode : Number of entries of "most" symbol
        """
        self.at = at if at else 0
        self.txt = txt if txt else ""
        self.n = 0
        self.has = {}
        self.most = 0
        self.mode = None

    def add(self, newSym):
        """
        Takes a string symbol as argument and adds it to the SYM's "has" counter. If
        the new symbol is the one with most entries "mode" and "most" are modified
        """
        if newSym != "?":
            self.n = self.n + 1
            self.has[newSym] = 1 + self.has.get(newSym, 0)
            if self.has[newSym] > self.most:
                self.most = self.has[newSym]
                self.mode = newSym

    def mid(self):
        """
        Returns mode
        """
        return self.mode

    def div(self):
        """
        Returns the Shannon Entropy of the Object's counter "has"
        """
        freqList = [i / sum(self.has.values()) for i in self.has.values()]
        entropies = [i * math.log(i, 2) for i in freqList]
        entropy = -sum(entropies)
        return entropy

    def rnd(self, x, n):
        return x

    def dist(self, s1, s2):
        if s1 == "?" and s2 == "?":
            return 1
        elif s1 == s2:
            return 0
        else:
            return 1