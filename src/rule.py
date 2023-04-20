class RULE: 
    def prune(rule, maxSize):
        n=0
        for txt,ranges in rule.items():
            n = n+1
            if len(ranges) == maxSize[txt]:
                n=n+1
                rule[txt] = None
        if n > 0:
            return rule 
    def RULE_SIZE(self,ranges,maxSize):
            t={}
            for range in ranges:
                t[range['txt']] = t.get(range['txt']) or []
                t[range['txt']].append({'lo' : range['lo'],'hi' : range['hi'],'at':range['at']})
            return self.prune(t, maxSize)
   