from sym import SYM
from misc import *

class RANGE:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.lo = lo
        self.hi = lo or hi or lo
        self.y = SYM()

    def extend(self, n, s):
        self.lo = min(n, self.lo)
        self.hi = max(n, self.hi)
        self.y.add(s)

def extend(range, n, s):
    range.lo = min(n, range.lo)
    range.hi = max(n, range.hi)
    range.y.add(s)

def bin(col,x):
    if x=='?' or isinstance(col, SYM):
        return x
    tmp = (col.hi - col.lo)/(the['bins'] - 1)
    return  1 if col.hi == col.lo else math.floor(x/tmp + .5)*tmp

def value(has, n_b, n_r, s_goal = None):
    b, r = 0, 0
    for x, n in has.items():
        if x == s_goal:
            b = b + n
        else:
            r = r + n
    b, r = b / (n_b + 1 / float('inf')), r / (n_r + 1 / float('inf'))
    return b ** 2 / (b + r)

def bins(cols,rowss):
    def rowsMapper(col):
        def xy(x,y):
            nonlocal n
            if x != '?':
                n = n + 1
                k = bin(col,x)
                ranges[k] = ranges.get(k,RANGE_1(col.at,col.txt,x))
                extend(ranges[k], x, y)
        n,ranges = 0,{}
        for y,rows in rowss.items():
            for _,row in enumerate(rows):
                xy(row.cells[col.at],y)
        return n, ranges
    
    def colsMapper(col):
        def itself(x):
            return x
        n,ranges = rowsMapper(col)
        ranges   = sorted(list(map(itself, ranges.values())),key = lambda x: x.lo)
        if   type(col) == SYM:
            return ranges 
        else:
            return merges(ranges, n/the['bins'], the['d']*col.div()) 
    
    ret = list(map(colsMapper, cols))
    return ret

def merge(col1, col2):
    new = deepcopy(col1)
    if isinstance(col1, SYM):
        for x, n in col2.has.items():
            new.add(x, n)
    else:
        for _, n in col2.has.items():
            new.add(n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new

def merge2(col1, col2):
    new = merge(col1, col2)
    if new.div() <= ((col1.div() * col1.n) + (col2.div() * col2.n)) / new.n:
        return new

def mergeAny(ranges0):
    def noGaps(t):
        if not t:
            return t
        for j in range(1, len(t)):
            t[j].lo = t[j - 1].hi
        t[0].lo = float('-inf')
        t[len(t) - 1].hi = float('inf')
        return t

    ranges1 = []
    j = 0
    while j < len(ranges0):
        left = ranges0[j]
        right = None if j == len(ranges0) - 1 else ranges0[j + 1]
        if right is not None:
            y = merge2(left.y, right.y)
            if y is not None:
                j += 1
                left.hi, left.y = right.hi, y
        ranges1.append(left)
        j += 1
    return noGaps(ranges0) if len(ranges0) == len(ranges1) else mergeAny(ranges1)

def merges(ranges0,nSmall,nFar):
    def merges2(left,right,j):
        y = merged(left.y, right.y, nSmall, nFar)
        if y: 
            j = j+1
            left.hi, left.y = right.hi, y
        return j , left

    def noGaps(t):
        if not t:
            return t
        for j in range(1,len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo  = float('-inf')
        t[len(t)-1].hi =  float('inf')
        return t

    ranges1,j,here = [],0, None
    while j < len(ranges0):
        here = ranges0[j]
        if j < len(ranges0)-1:
            j,here = merges2(here, ranges0[j+1], j)
        j=j+1
        ranges1.append(here)
    return noGaps(ranges0) if len(ranges0)==len(ranges1) else merges(ranges1,nSmall,nFar)

def merged(col1,col2,nSmall, nFar):
    new = merge(col1,col2)
    if nSmall and col1.n < nSmall or col2.n < nSmall:
        return new
    if nFar   and not type(col1) == SYM and abs(col1.div() - col2.div()) < nFar:
        return new
    if new.div() <= (col1.div()*col1.n + col2.div()*col2.n)/new.n:
        return new

def merge(col1,col2):
    new = deepcopy(col1)
    if type(col1) == SYM:
        for x,n in col2.has.items():
            new.add(x)
    else:
        for _,n in enumerate(col2.has):
            new.add(n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new