from misc import *
from data import *

def half(self, rows = None, cols = None, above = None):
    def gap(row1,row2): 
        return self.dist(row1,row2,cols)
    def project(row):
        return {'row' : row, 'dist' : cosine(gap(row,A), gap(row,B), c)}
    rows = rows or self.rows
    some = many(rows,the['Halves'])
    A    = above if above and the['Reuse'] else any(some)
    tmp = sorted([{'row': r, 'dist': gap(r, A)} for r in some], key=lambda x: x['dist'])
    far = tmp[int((len(tmp) - 1) * the['Far'])]
    B    = far['row']
    c    = far['dist']
    left, right = [], []
    for n,tmp in enumerate(sorted(map(project, rows), key=lambda x: x['dist'])):
        if (n + 1) <= (len(rows) / 2):
            left.append(tmp["row"])
        else:
            right.append(tmp["row"])
    evals = 1 if the['Reuse'] and above else 2
    return left, right, A, B, c, evals   
    
def sway(self):
    data = self
    def worker(rows, worse, evals0 = None, above = None):
        if len(rows) <= len(data.rows)**the['min']: 
            return rows, many(worse, the['rest']*len(rows)), evals0
        else:
            l,r,A,B,c,evals = self.half(rows, None, above)
            if self.better(B,A):
                l,r,A,B = r,l,B,A
            for row in r:
                worse.append(row)
            return worker(l,worse,evals+evals0,A)
    best,rest,evals = worker(data.rows,[],0)
    return DATA.clone(self, best), DATA.clone(self, rest), evals