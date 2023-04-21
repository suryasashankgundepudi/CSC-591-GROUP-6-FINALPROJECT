from misc import *
import copy
from config import *
from data import *
from utils import *
from optimize import OPTIMIZE

def main():

    global args
    seedarr = [
        937162211, 6541321, 9879653, 9362224, 937162268,
        936162874, 6662211, 21352211, 77632211, 933362211,
        9376442211, 541321, 33879653, 7265224, 6222158,
        630148470, 51327910, 989462111, 7054511, 9332211
    ]
    result_array = []

    for seed in seedarr:
        
        args = OPTIMIZE.getCliArgs(seed)
        print(args)
        result = OPTIMIZE.xplnFunc()
        result_array.append(result)


    all_stats = {'all': {}, 'sway1': {}, 'sway2': {}, 'xpln1': {}, 'xpln2': {}, 'top': {}}
    var_dic = {key: [] for key in result_array[0]['all'].keys()}
    data_store = {key: copy.deepcopy(var_dic) for key in all_stats.keys()}

    for result in result_array:
        for key, value in result.items():
            for sub_key, sub_value in value.items():
                all_stats[key][sub_key] = all_stats[key].get(sub_key, 0) + sub_value
                data_store[key][sub_key].append(sub_value)

    print('*********************************\nDataset: {}\n********************************'.format(result_array[0]['args'].file.split('/')[-1]))
    print('Mean results of best outcomes from 20 runs\n************************************\n')
    print("\t",'\t'.join(all_stats['all'].keys()))
    for key in all_stats.keys():
        print("{}\t".format(key),'\t'.join([str(round(all_stats[key][i]/len(seedarr), 2)) for i in all_stats[key].values()]))

    print('\n')
    print('\n')
    print('**********************************\nSize Comparison - Cliffs Delta\n************************************')
    print("\t\t",'\t'.join(all_stats['all'].keys()))
    for i in [('all', 'all'), ('all', 'sway1'), ('all', 'sway2'), ('sway1', 'sway2'), ('sway1', 'xpln1'), ('sway2', 'xpln2'), ('sway1', 'top')]:
        effect_sizes = [cliffsDelta(data_store[i[0]][j], data_store[i[1]][j]) for j in all_stats['all'].keys()]
        output = ['=' if size else '≠' for size in effect_sizes]
        print("{} to {}\t{}".format(i[0], i[1], '\t'.join(output)))


if __name__ == "__main__":
    main()
