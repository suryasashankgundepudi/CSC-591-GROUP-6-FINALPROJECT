import sys, re, math
from test_all_HW6 import *
from misc import *
from config import *


def main():
    saved, fails = {}, 0
    for k, v in cli(settings(help)).items():
        the[k] = v
        saved[k] = v
    if the['help']:
        print(help)
    else:
        for what, fun in egs.items():
            if the['go'] == 'all' or the['go'] == what:
                for k, v in saved.items():
                    the[k] = v
                Seed = the['seed']
                if not egs[what]():
                    fails += 1
                    print('❌ Fail:', what)
                else:
                    print('✅ Pass:', what)
    sys.exit(fails)


if __name__ == "__main__":
    eg("the", "testng the", test_the())
    eg("sym", "testing the sym class", test_sym())
    eg("num", "testing the num class", test_num())
    eg("rand", "testing Random function", test_rand())
    eg("csv", "testing CSV Function", test_csv())
    eg("data", "testing DATA for reading csv", test_data())
    eg("clone", "replicate structure of a DATA", test_clone())
    eg('cliffs', 'start tests', test_cliffs())
    eg('dist', 'distance test', test_dist())
    eg('bins', 'find deltas between best and rest', test_bins())
    eg('xpln', 'explore explanation sets', test_xpln())
    eg('tree', 'make snd show tree of clusters', test_tree())
    eg('sway', 'optimizing', test_sway())
    eg("half", "divide data in half", test_half())
    main()
