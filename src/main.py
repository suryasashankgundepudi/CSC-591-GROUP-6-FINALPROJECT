import sys, re, math
from misc import *
from config import *
from discrete import *
from sway import *


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
    # eg('xpln1', 'explore explanation sets1', xpln1())
    eg('sway1', 'optimizing1', sway())
    # eg('xpln2', 'explore explanation sets2', xpln2())
    eg('sway2', 'optimizing2', sway())
    main()
