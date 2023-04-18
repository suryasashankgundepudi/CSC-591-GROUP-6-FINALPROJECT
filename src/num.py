import math
from numerics import *


class NUM:
    def __init__(self, at=None, txt=None):
        """
        Constructor for NUM Class
        count : To count number of entries
        mu : mean of all entered values
        m2 : Standard Deviation
        lo : lowest numerical entry
        hi : highest numerical entry
        """
        self.at = at if at else 0
        self.txt = txt if txt else ""
        self.n = 0
        self.count, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = math.inf, -math.inf
        self.w = -1 if "-" in self.txt else 1


    def add(self, n):
        """
        Function to add an entry to the NUM object.
        Recalculates mean (mu) and std dev (m2).
        """
        if n != "?":
            self.count += 1
            d = n - self.mu
            self.mu += d / self.count
            self.m2 += d * (n - self.mu)
            self.lo = min(self.lo, n)
            self.hi = max(self.hi, n)

    def mid(self):
        """
        Returns the mean (mu)
        """
        return self.mu

    def div(self):
        """
        Returns the Standard Deviation
        """
        if self.m2 < 0 or self.n < 2:
            return 0
        else:
            return (self.m2 / (self.n - 1)) ** 0.5

    def rnd(self, x, n):
        if x == "?":
            return x
        else:
            return rnd(x, n)

    def norm(self, n):
        return n if n == "?" else (n - self.lo) / (self.hi - self.lo + 1e-32)

    def dist(self, n1, n2):
        if n1 == "?" and n2 == "?":
            return 1
        n1, n2 = self.norm(n1), self.norm(n2)
        if n1 == "?":
            n1 = 1 if n2 < 0.5 else 0
        if n2 == "?":
            n2 = 1 if n1 < 0.5 else 0
        return abs(n1 - n2)
