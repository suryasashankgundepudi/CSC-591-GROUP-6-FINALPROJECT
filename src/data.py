from misc import *
from row import ROW
from col import COL
from config import *
from numerics import *
import math


class DATA:
    def __init__(self, src):
        """
        Initializing function for data class object.
        A container for self.rows to be summarized in self.cols
        """
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            csv(src, self.add)
        else:
            for i in src:
                self.add(i)

    def add(self, t):
        """
        Add a new row and update the column headers
        """
        if self.cols:
            if isinstance(t, list):
                t = ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COL(t)

    def clone(self, init = {}):
        """
        For cloning the DATA object with the same structure as init
        """
        data = DATA([self.cols.names])
        _ = list(map(data.add, init))
        return data

    def stats(self, what, cols, nPlaces):
        """
        Function for returning a certain attribute or certain stats
        for a column in data
        """

        def fun(_, col):
            if what == 'div':
                val = col.div()
            else:
                val = col.mid()
            return col.rnd(val, nPlaces),col.txt
        return kap(cols or self.cols.y, fun)


    def dist(self, row1, row2, cols=None):
        """
        Function for returning the distance between two rows.
        Returns a float which is the distance between row 1 and row 2
        """
        n, d = 0, 0
        cols = cols if cols else self.cols.x
        for col in cols:
            n = n + 1
            d = d + (col.dist(row1.cells[col.at], row2.cells[col.at]) ** the['p'])
            
        return (d / n) ** (1 / the['p'])
    

    def around(self, row1, rows=None, cols=None):
        """
        Sorting rows by the distance to row1
        """

        def func(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        return sorted(list(map(func, rows or self.rows)), key=itemgetter("dist"))

    def half(self, rows=None, cols=None, above=None):
        """
        Divides the data with 2 points
        """

      
    def half(self, rows = None, cols = None, above = None):
        def gap(row1,row2): 
            return self.dist(row1,row2,cols)
        def project(row):
            return {'row' : row, 'dist' : cosine(gap(row,A), gap(row,B), c)}
        rows = rows or self.rows
        some = many(rows,the['Halves'])
        A    = above if above and the['Reuse'] else any(some)
        def function(r):
            return {'row' : r, 'dist' : gap(r, A)}
        tmp = sorted(list(map(function, some)), key=itemgetter('dist'))
        far = tmp[int(the['Far'] * len(rows))//1]
        B    = far['row']
        c    = far['dist']
        left, right = [], []
        for n,tmp in enumerate(sorted(list(map(project, rows)), key=itemgetter('dist'))):
            if n < len(rows)//2:
                left.append(tmp['row'])
            else:
                right.append(tmp['row'])
        evals = 1 if the['Reuse'] and above else 2
        return left, right, A, B, c, evals
        
    def cluster(self, rows=None, cols=None, above=None):
        """
        Returns rows recursively halved
        """
        rows = rows or self.rows
        cols = cols or self.cols.x
        node = {'data': self.clone(rows)}

        if len(rows) >=2:
            left, right, node['A'], node['B'], node["mid"], _ = self.half(rows, cols, above)
            node['left'] = self.cluster(left, cols, node['A'])
            node['right'] = self.cluster(right, cols, node['B'])
        return node

    def better(self, row1, row2):
         s1,s2,ys = 0, 0, self.cols.y
         for col in ys:
            x  = col.norm(row1.cells[col.at])
            y  = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
         return s1/len(ys) < s2/len(ys)


    def sway(self):
    #     """
    #     Returns the better half recursively
    #     """        
        data = self
        def sway1(rows, worse, evals0 = None, above = None):
            if len(rows) <= len(data.rows)**the['min']: 
                return rows, many(worse, the['rest']*len(rows)), evals0
            else:
                l,r,A,B,c,evals = self.half(rows, None, above)
                if self.better(B,A):
                    l,r,A,B = r,l,B,A
                for row in r:
                    worse.append(row)
                return sway1(l,worse,evals+evals0,A)
        best,rest,evals = sway1(data.rows,[],0)
        return self.clone(best), self.clone(rest), evals


    def tree(self, rows = None , min = None, cols = None, above = None):
        rows = rows or self.rows
        min  = min or len(rows)**the['min']
        cols = cols or self.cols.x
        node = { 'data' : self.clone(rows) }
        if len(rows) >= 2*min:
            left, right, node['A'], node['B'], _, _ = self.half(rows,cols,above)
            node['left']  = self.tree(left,  min, cols, node['A'])
            node['right'] = self.tree(right, min, cols, node['B'])
        return node
    
    def xpln(self,best,rest):
        tmp,maxSizes = [],{}
        def v(has):
            return value(has, len(best.rows), len(rest.rows), "best")
        def score(ranges):
            rule = self.RULE_SIZE(ranges,maxSizes)
            if rule:
                print(self.showRule(rule))
                bestr= self.selects(rule, best.rows)
                restr= self.selects(rule, rest.rows)
                if len(bestr) + len(restr) > 0: 
                    return v({'best': len(bestr), 'rest':len(restr)}),rule
        for ranges in bins(self.cols.x,{'best':best.rows, 'rest':rest.rows}):
            maxSizes[ranges[0]['txt']] = len(ranges)
            print("")
            for range in ranges:
                print(range['txt'], range['lo'], range['hi'])
                tmp.append({'range':range, 'max':len(ranges),'val': v(range['y'].has)})
        rule,most=firstN(sorted(tmp, key=itemgetter('val')),score)
        return rule,most
    
    def showRule(self,rule):
        def pretty(range):
            return range['lo'] if range['lo']==range['hi'] else [range['lo'], range['hi']]
        def merge(t0):
            t,j =[],1
            while j<=len(t0):
                left = t0[j-1]
                if j < len(t0):
                    right = t0[j]
                else:
                    right = None
                if right and left['hi'] == right['lo']:
                    left['hi'] = right['hi']
                    j=j+1
                t.append({'lo':left['lo'], 'hi':left['hi']})
                j=j+1
            return t if len(t0)==len(t) else merge(t) 
        def merges(attr,ranges):
            return list(map(pretty,merge(sorted(ranges,key=itemgetter('lo'))))),attr
        return dkap(rule,merges)
    
    def RULE_SIZE(self,ranges,maxSize):
        t={}
        for range in ranges:
            t[range['txt']] = t.get(range['txt']) or []
            t[range['txt']].append({'lo' : range['lo'],'hi' : range['hi'],'at':range['at']})
        return prune(t, maxSize)
    
    def betters(self,n):
        tmp=sorted(self.rows, key=lambda row: self.better(row, self.rows[self.rows.index(row)-1]))
        return  n and tmp[0:n], tmp[n+1:]  or tmp

    def selects(self, rule, rows):
        def disjunction(ranges, row):
            for range in ranges:
                lo, hi, at = range['lo'], range['hi'], range['at']
                x = row.cells[at]
                if x == "?":
                    return True
                if lo == hi and lo == x:
                    return True
                if lo <= x and x < hi:
                    return True
            return False

        def conjunction(row):
            for ranges in rule.values():
                if not disjunction(ranges, row):
                    return False
            return True

        def function(r):
            if conjunction(r):
                return r

        return list(map(function, rows))