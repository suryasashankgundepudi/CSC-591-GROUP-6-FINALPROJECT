from col import COL
import utils
import random

def row(data, t):
    if data.cols:
        data.rows.append(t)
        for col in [data.cols.x, data.cols.y]:
            for c in col:
                add(c, t[c.at])
    else:
        data.cols = COL(t)
    return data

def add(col, x, n=None):
    def sym(t):
        t[x] = n + (t.get(x, 0))
        if t[x] > col.most:
            col.most, col.mode = t[x], x

    def num(t):
        col.lo, col.hi = min(x, col.lo), max(x, col.hi)
        if len(t) < utils.args.Max:
            col.ok = False
            t.append(x)
        elif random.random() < utils.args.Max / col.n:
            col.ok = False
            t[random.randint(0, len(t) - 1)] = x

    if x != "?":
        n = n or 1
        col.n += n
        if isinstance(col, COL) and col.isSym:
            sym(col.has)
        else:
            x = float(x)
            num(col.has)

def adds(col, t):
    for value in t or []:
        add(col, value)
    return col

def extend(range_, n, s):
    range_.lo = min(n, range_.lo)
    range_.hi = max(n, range_.hi)
    add(range_.y, s)
