import misc
from row import ROW
from col import COL
from config import *
from numerics import *
import math
from rule import *
import csv
import os
import random
from utils import *

class DATA:
    def __init__(self, src, rows = None):
        self.rows = []
        self.cols = None
        add = lambda t: row(self, t)
        print("@11",add)
        print("@12",src)
        src="C:/Users/91918/Desktop/ASE_Project/CSC-591-GROUP-6-FINALPROJECT/etc/data/auto2.csv"
        print("@13",src)
        if isinstance(src, str):
            self.readcsv(add)
        else:
            self.cols = COL(src.cols.names)
            if rows:
                for row in rows:
                    add(row)

    def row(data, t):
        if data.cols:
            data.rows.append(t)
            for col in [data.cols.x, data.cols.y]:
                for c in col:
                    DATA.add(c, t[c.at])
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
        return misc.kap(cols or self.cols.y, fun)


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

        return sorted(list(map(func, rows or self.rows)), key=misc.itemgetter("dist"))

    def readcsv(sFilename, fun):
        with open(sFilename, mode='r') as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                fun(line)
      
    def half(self, rows = None, cols = None, above = None):
        def gap(row1,row2): 
            return self.dist(row1,row2,cols)
        def project(row):
            return {'row' : row, 'dist' : cosine(gap(row,A), gap(row,B), c)}
        rows = rows or self.rows
        some = misc.many(rows,the['Halves'])
        A    = above if above and the['Reuse'] else any(some)
        def function(r):
            return {'row' : r, 'dist' : gap(r, A)}
        tmp = sorted(list(map(function, some)), key=misc.itemgetter('dist'))
        far = tmp[int(the['Far'] * len(rows))//1]
        B    = far['row']
        c    = far['dist']
        left, right = [], []
        for n,tmp in enumerate(sorted(list(map(project, rows)), key=misc.itemgetter('dist'))):
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
                return rows, misc.many(worse, the['rest']*len(rows)), evals0
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
            return list(map(pretty,merge(sorted(ranges,key=misc.itemgetter('lo'))))),attr
        return misc.dkap(rule,merges)
    
    
    def betters(self,n):
        tmp=sorted(self.rows, key=lambda row: self.better(row, self.rows[self.rows.index(row)-1]))
        return  n and tmp[0:n], tmp[n+1:]  or tmp
    
    
    

