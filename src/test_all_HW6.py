from misc import *
from num import NUM
from numerics import *
from sym import SYM
from config import *
from data import *
from main import *


def eg(key, str, fun):
    """
    Example function for running the test cases. Takes in key, string and function that needs to be tested
    """
    egs[key] = fun
    global help
    help = help + '  -g ' + key + '\t' + str + '\n'



def test_rand():
    """
    Function for checking if rand function works or not
    """
    n1, n2 = NUM(), NUM()
    global Seed
    Seed = the['seed']
    for i in range(1, 10 ** 3 + 1):
        n1.add(rand(0, 1))
    Seed = the['seed']
    for i in range(1, 10 ** 3 + 1):
        n2.add(rand(0, 1))
    m1, m2 = rnd(n1.mid(), 1), rnd(n2.mid(), 1)
    print("✅pass rand")
    return m1 == m2 and .5 == rnd(m1, 1)
    


def test_sym():
    """
    Function for checking if the SYM Class works  and for checking if div/mid functions work
    """
    sym = SYM()
    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)
    print("✅pass sym ")
    return "a" == sym.mid() and 1.379 == rnd(sym.div())


def test_num():
    """
    Function for checking if the NUM class works and if div and mid functions work
    """
    num = NUM()
    for x in [1, 1, 1, 1, 2, 2, 3]:
        num.add(x)
    print("✅pass num ")
    return 11 / 7 == num.mid() and 0.787 == rnd(num.div())


def test_the():
    """
    Function to print the options for the code
    """
    print(the.__repr__())
    print("✅pass the")


def test_csv():
    """
    Function for testing the CSV function
    """
    n = 0

    def f(t):
        nonlocal n
        n += len(t)

    csv(the["file"], f)
    print("✅pass csv")
    return n == 8 ** 399


def test_data():
    """
    Function for testing the data class
    """
    data = DATA(the['file'])
    col=data.cols.x[0]
    
    
    
    print("✅pass data")
    return len(data.rows) == 398 and data.cols.x[1].at == 1 and len(data.cols.x) == 4




def test_clone():
    data1 = DATA(the['file'])
    data2 = data1.clone(data1.rows)
    print(data1.stats('mid', data1.cols.y, 2))
    print(data2.stats('mid', data2.cols.y, 2))
    print("✅pass clone")



def test_half():
   data = DATA(the['file'])
   left,right,A,B,c,_ = data.half() 
   
   print(len(left),len(right))
   
   l,r = data.clone(left), data.clone(right)
   print("l",l.stats('mid', l.cols.y, 2))
   print("r",r.stats('mid', r.cols.y, 2))
   print("✅pass half")

    
def test_cliffs():
    assert(False == cliffsDelta( [8,7,6,2,5,8,7,3],[8,7,6,2,5,8,7,3]))
    assert(True  == cliffsDelta( [8,7,6,2,5,8,7,3], [9,9,7,8,10,9,6])) 
    t1,t2=[],[]
    for i in range(1,1000+1):
        t1.append(rand(0,1))
    for i in range(1,1000+1):
        t2.append(rand(0,1)**.5)
    assert(False == cliffsDelta(t1,t1)) 
    assert(True  == cliffsDelta(t1,t2)) 
    diff,j=False,1.0
    while not diff:
        def function(x):
            return x*j
        t3=list(map(function, t1))
        diff=cliffsDelta(t1,t3)
        print(">",rnd(j),diff) 
        j=j*1.025
    print("✅pass cliffs")
        
def test_dist():
    data = DATA(the['file'])
    num  = NUM()
    for row in data.rows:
        num.add(data.dist(row, data.rows[1]))
    print({'lo' : num.lo, 'hi' : num.hi, 'mid' : rnd(num.mid()), 'div' : rnd(num.div())})   
    print("✅pass dist")
    
def test_xpln():
    data = DATA(the['file'])
    best,rest,evals = data.sway()
    rule,most= data.xpln(best,rest)
    print("explain=", data.showRule(rule))
    selects = data.selects(rule,data.rows)
    data_selects = [s for s in selects if s!=None]
    data1= data.clone(data_selects)
    print("all               ",data.stats('mid', data.cols.y, 2),data.stats('div', data.cols.y, 2))
    print("sway with",evals,"evals",best.stats('mid', best.cols.y, 2),best.stats('div', best.cols.y, 2))
    print("xpln on",evals,"evals",data1.stats('mid', data1.cols.y, 2),data1.stats('div', data1.cols.y, 2))
    top,_ = data.betters(len(best.rows))
    top = data.clone(top)
    print("sort with",len(data.rows),"evals",top.stats('mid', top.cols.y, 2),top.stats('div', top.cols.y, 2))   
    print("✅pass xlpn")
    
def test_tree():
    data = DATA(the['file'])
    showTree(data.tree(),"mid",data.cols.y,1)
    print("✅pass tree")
    return True

def test_sway():
    data = DATA(the['file'])
    best,rest,_ = data.sway()
    print("\nall ", data.stats('mid', data.cols.y, 2))
    print("    ", data.stats('div', data.cols.y, 2))
    print("\nbest",best.stats('mid', best.cols.y, 2))
    print("    ", best.stats('div', best.cols.y, 2))
    print("\nrest", rest.stats('mid', rest.cols.y, 2))
    print("    ", rest.stats('div', rest.cols.y, 2))
    print("✅pass sway")
    return True

def test_bins():
    global b4
    data = DATA(the['file'])
    best,rest,_ = data.sway()
    print("all","","","",{'best':len(best.rows), 'rest':len(rest.rows)})
    for k,t in enumerate(bins(data.cols.x,{'best':best.rows, 'rest':rest.rows})):
        for range in t:
            if range['txt'] != b4:
                print("")
            b4 = range['txt']
            print(range['txt'],range['lo'],range['hi'],
            rnd(value(range['y'].has, len(best.rows),len(rest.rows),"best")), 
            range['y'].has)  
    print("✅pass bins")   
