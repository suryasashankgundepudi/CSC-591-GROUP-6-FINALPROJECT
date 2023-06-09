from range import value, bins
from misc import *
from rule import RULE

class XPLN:
    def __init__(self, best, rest):
        self.tmp = []
        self.maxSizes = {}
        self.best = best
        self.rest = rest

    def xpln1(self, data, best, rest):
        def v(has):
            return value(has, len(best.rows), len(rest.rows), 'best')
        def score(self, ranges):
            rule = RULE.RULE_SIZE(self,ranges, self.maxSizes)
            if rule:
                bestr = self.selects(rule, self.best.rows)
                restr = self.selects(rule, self.rest.rows)
                if len(bestr) + len(restr) > 0:
                    return value({'best': len(bestr), 'rest': len(restr)}, len(self.best.rows), len(self.rest.rows), 'best'), rule
        tmp,self.maxSizes = [],{}
        for _,ranges in enumerate(bins(data.cols.x,{'best':best.rows, 'rest':rest.rows})):
            self.maxSizes[ranges[0].txt] = len(ranges)
            for _,range in enumerate(ranges):
                tmp.append({'range':range, 'max':len(ranges),'val': v(range.y.has)})
        rule,most=self.firstN1(sorted(tmp,key = lambda x: x['val'],reverse=True),score)
        return rule,most  
    
    def xpln2(self, data, best, rest):
        def v(has):
            return value(has, len(best.rows), len(rest.rows), 'best')
        def score(ranges, negranges):
            rule = {'pos':RULE.RULE_SIZE(self,ranges, maxSizes), 'neg':RULE.RULE_SIZE(self,negranges, maxSizes)}
            if rule['pos']:
                bestr= self.selects2(rule, best.rows)
                restr= self.selects2(rule, rest.rows)
                if len(bestr) + len(restr) > 0:
                    return v({"best": len(bestr), "rest": len(restr)}), rule
        tmp, maxSizes = [], {}
        for ranges in bins(data.cols.x, {'best': best.rows, 'rest': rest.rows}):
            ranges = list(ranges.values()) if isinstance(ranges, dict) else ranges
            maxSizes[ranges[0].txt] = len(ranges)
            for range in ranges:
                tmp.append({'range': range, 'max': len(ranges), 'val': v(range.y.has)})

        rule, most = self.firstN2(sorted(tmp, key=lambda x: x["val"], reverse=True), score)
        return rule, most 
    
    def firstN1(self, sorted_ranges, scoreFun):
        first = sorted_ranges[0]['val']

        def useful(range):
            if range['val'] > 0.05 and range['val'] > first / 10:
                return range
        sorted_ranges = [s for s in sorted_ranges if useful(s)]
        most = -1
        out = -1
        for n in range(len(sorted_ranges)):
            tmp, rule = scoreFun([r['range'] for r in sorted_ranges[:n+1]])
            if tmp is not None and tmp > most:
                out, most = rule, tmp
        return out, most
    
    def firstN2(self, sorted_ranges, scoreFun):
        first = sorted_ranges[0]['val']

        def useful(range):
            if range['val'] > 0.05 and range['val'] > first / 10:
                return range
            
        def neg(range):
            if range['val'] < 0.05 and range['val'] < first / 10:
                return range

        negranges = list(filter(neg, sorted_ranges))
        negranges.reverse()
        sorted_ranges = list(filter(useful, sorted_ranges))
        sorted_ranges = [s for s in sorted_ranges if useful(s)]
        most,out = -1,-1
        for n in range(len(sorted_ranges)):
            tmp, rule = scoreFun([r['range'] for r in sorted_ranges[:n+1]])
            if tmp is not None and tmp > most:
                out, most = rule, tmp
        return out, most
    
    def showRule(rule):
        def pretty(range):
            return range['lo'] if range['lo'] == range['hi'] else [range['lo'], range['hi']]
        def merges(attr, ranges):
            return list(map(pretty, merge(sorted(ranges, key=lambda x: x['lo'])))), attr
        def merge(t0):
            t = []
            j = 0
            while j < len(t0):
                left = t0[j]
                right = None if j+1 >= len(t0) else t0[j+1]
                if right and left['hi'] == right['lo']:
                    left['hi'] = right['hi']
                    j = j +  1
                t.append({'lo': left['lo'], 'hi': left['hi']})
                j = j +  1
            return t if len(t0) == len(t) else merge(t)
        return kap(rule, merges)

    def selects(rule, rows):
        def disjunction(ranges, row):
            for rang in ranges:
                at = rang['at']
                x = row.cells[at]
                lo = rang['lo']
                hi = rang['hi']  
                if x == '?' or (lo == hi and lo == x) or (lo <= x and x< hi):
                    return True
            return False

        def conjunction(row):
            for _,ranges in rule.items():
                if not disjunction(ranges, row):
                    return False
            return True

        def function(r):
            return r if conjunction(r) else None
        
        r = []
        for item in list(map(function, rows)):
            if item:
                r.append(item)
        return r

    def selects2(rule, rows):
        def disjunction(ranges, row):
            for rang in ranges:
                at = rang['at']
                x = row.cells[at]
                lo = rang['lo']
                hi = rang['hi']  
                if x == '?' or (lo == hi and lo == x) or (float(lo) <= float(x) and float(x)< float(hi)):
                    return True
                if x.replace(".", "").isnumeric():
                    x = float(x) 
                else:
                    x
            return False

        def conjunction(row):
            if rule:
                for ranges in rule['pos'].values():
                    for neg in rule['neg'].values():
                        if disjunction(neg, row):
                            return False
                    if not disjunction(ranges, row):
                        return False
                return True
            else:
                return True

        def function(r):
            return r if conjunction(r) else None
        
        r = []
        for item in list(map(function, rows)):
            if item:
                r.append(item)
        return r