the = {
    'dump': False,
    'go': None,
    'seed': 937162211,
    'file': "/Users/harshithaparuchuri/Documents/NCSU/sem2/ASE/ASE591-HW_GP6-9/etc/data/auto93.csv",
    "Halves": 512,
    "p":2,
    "Far":.95,
    "Reuse":True,
    "cliffs": .147,
    "min":.5,
    "rest":4,
    "bins":16,
    'bootstrap':512, 
    'conf':0.05, 
    'cliff':.4, 
    'cohen':.35,
    'Fmt': "{:.2f}", 
    'width':40,
    'n_iter': 20

}

help = '''USAGE: python main.py  [OPTIONS] [-g ACTION]
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -f  --file    data file                    = ../../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
    '''

egs = {}

Seed = 937162211

n = 0

b4 = []


table_1 = {'all': {'data' : [], 'evals' : 0},
             'sway1': {'data' : [], 'evals' : 0},
             'sway2': {'data' : [], 'evals' : 0},
             'xpln1': {'data' : [], 'evals' : 0},
             'xpln2': {'data' : [], 'evals' : 0},
             'top': {'data' : [], 'evals' : 0}}

table_2 = [[['all', 'all'],None],
                [['all', 'sway1'],None],
                [['sway1', 'sway2'],None],
                [['sway1', 'xpln1'],None],
                [['sway2', 'xpln2'],None],
                [['sway1', 'top'],None]]





