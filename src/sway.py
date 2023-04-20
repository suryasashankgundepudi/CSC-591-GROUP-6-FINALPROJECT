from misc import *
from data import *
import numpy as np
from sklearn.cluster import KMeans
import random
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

def bdom(self, rows1, rows2, ys=None):
    if isinstance(rows1, ROW):
        rows1 = [rows1]
        rows2 = [rows2]
    if not ys:
        ys = self.cols.y
    
    for col in ys:
        dominates = all(
            col.norm(row1.cells[col.at]) * col.w * -1 <= col.norm(row2.cells[col.at]) * col.w * -1
            for row1, row2 in zip(rows1, rows2)
        )
        if not dominates:
            return False
    return True

def better_bdom(self, row1, row2, ys=None):
    return self.bdom([row1], [row2], ys=ys) and not self.bdom([row2], [row1], ys=ys)

def kmeans(self, rows=None):
    if not rows:
        rows = self.rows
        
    row_set = np.array([r.cells for r in rows])
    kmeans = KMeans(n_clusters=2, random_state=the['seed'], n_init=10).fit(row_set)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    left_cluster = ROW(centers[0])
    right_cluster = ROW(centers[1])
    def min_dist(center, rows, labels, cluster_id):
        closest_row = None
        closest_distance = float('inf')
        for i, row in enumerate(rows):
            if labels[i] == cluster_id:
                distance = self.dist(row, center)
                if distance < closest_distance:
                    closest_row = row
                    closest_distance = distance
        return closest_row
    A = min_dist(left_cluster, rows, labels, 0)
    B = min_dist(right_cluster, rows, labels, 1)

    left = [rows[i] for i in range(len(rows)) if labels[i] == 0]
    right = [rows[i] for i in range(len(rows)) if labels[i] == 1]

    return left, right, A, B, 1





def sway(self,clus='half',better='zitler'):
    data = self
    def worker(rows, worse, evals0 = None, above = None):
        if len(rows) <= len(data.rows)**the['min']: 
            return rows, many(worse, the['rest']*len(rows)), evals0
        else:
            #we are using half(default in sway) and Kmeans algorithm to compare the results and check whether its optimizing the result or not
            if clus=='half':
                l,r,A,B,c,evals = half(rows, None, above)
            elif clus=='kmeans':
                l,r,A,B,evals=kmeans(rows)
            if better=='zitler':
                if self.better(B,A):
                    l,r,A,B = r,l,B,A
            elif better=='bdom':
                if self.better(B,A):
                    l,r,A,B = r,l,B,A       
 
            
            for row in r:
                worse.append(row)
            return worker(l,worse,evals+evals0,A)
    best,rest,evals = worker(data.rows,[],0)
    return DATA.clone(self, best), DATA.clone(self, rest), evals