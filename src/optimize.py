import argparse
from misc import *
from data import *
import numpy as np
from sklearn.cluster import KMeans
import random
from discrete import XPLN
import os
import random
import data as dt

class OPTIMIZE :
    Seed = None
    args = None
    n = 0
    egs = {}

    def half(self, rows = None, cols = None, above = None):
        def gap(row1,row2): 
            return self.dist(row1,row2,cols)
        def cosine(a,b,c):
            if c == 0:
                return 0
            return (a ** 2 + c ** 2 - b ** 2) / (2 * c)
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
                    l,r,A,B,c,evals = self.half(rows, None, above)
                elif clus=='kmeans':
                    l,r,A,B,evals=self.kmeans(rows)
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
    


    def getCliArgs(seed):
        print(seed)
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-b",
            "--bins",
            type=int,
            default=16,
            required=False,
            help="initial number of bins",
        )
        parser.add_argument(
            "-d",
            "--d",
            type=float,
            default=0.35,
            required=False,
            help="different is over sd*d",
        )
        parser.add_argument(
            "-g", "--go", type=str, default="all", required=False, help="start-up action"
        )
        parser.add_argument(
            "-h", "--help", action="store_true", help="show help"
        )
        parser.add_argument(
            "-s",
            "--seed",
            type=int,
            default=seed,
            required=False,
            help="random number seed",
        )
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            default="../etc/data/healthCloseIsses12mths0001-hard.csv",
            required=False,
            help="data file",
        )
        parser.add_argument(
            "-p",
            "--p",
            type=int,
            default=2,
            required=False,
            help="distance coefficient",
        )
        parser.add_argument(
            "-c",
            "--cliffs",
            type=float,
            default=0.147,
            required=False,
            help="cliff's delta threshold"

        )
        args = parser.parse_args()
        return args
        
    def xplnFunc():

        global Seed
        # Seed = OPTIMIZE.args.seed
        args=OPTIMIZE.getCliArgs(Seed)
        result = {}
        script_dir = os.path.dirname(__file__)
        full_path = os.path.join(script_dir, args.file)
        data = dt.DATA(full_path)
        sway_best, sway_rest, evals = OPTIMIZE.sway()
        result['all'] = data.stats(data)
        result['sway1'] = data.stats(sway_best)
        rule, _ = XPLN.xpln1(data, sway_best, sway_rest)
        data1 = dt.DATA(data, XPLN.selects(rule, data.rows))
        result['xpln1'] = data.stats(data1)
        top, _ = data.betters(data, 1)
        top = dt.DATA(data, top)
        result['top'] = data.stats(top)
        full_path = os.path.join(script_dir, args.file)
        data = dt.DATA(full_path)
        sway_best, sway_rest, evals = OPTIMIZE.sway('kmeans')
        result['sway2'] = data.stats(sway_best)
        rule, _ = XPLN.xpln2(data, sway_best, sway_rest)
        data1 = dt.DATA(data, XPLN.selects2(rule, data.rows))
        result['xpln2'] = data.stats(data1)

        return result  
        