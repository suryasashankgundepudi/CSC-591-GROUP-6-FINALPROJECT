import argparse
import csv
import json
import math
import os
import random
from site import sethelper
from num import NUM
from data import DATA
from operations import *
import range
import optimize as opt
import discrete as disc
from optimize import OPTIMIZE
from discrete import XPLN


args = None
Seed = None
n = 0
egs = {}

def getCliArgs(seed):
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

def xplnFunc(args):
    global Seed
    Seed=utils.args.seed
    result = {}
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, args)
    data = DATA(full_path)
    sway_best, sway_rest, evals = OPTIMIZE.sway()
    result['all'] = data.stats(data)
    result['sway1'] = data.stats(sway_best)
    rule, _ = XPLN.xpln1(data, sway_best, sway_rest)
    data1 = DATA(data, XPLN.selects(rule, data.rows))
    result['xpln1'] = data.stats(data1)
    top, _ = data.betters(data, 1)
    top = DATA(data, top)
    result['top'] = data.stats(top)
    full_path = os.path.join(script_dir, args)
    data = DATA(full_path)
    sway_best, sway_rest, evals = OPTIMIZE.sway('kmeans')
    result['sway2'] = data.stats(sway_best)
    rule, _ = XPLN.xpln2(data, sway_best, sway_rest)
    data1 = DATA(data, XPLN.selects2(rule, data.rows))
    result['xpln2'] = data.stats(data1)

    return result

    def csv_1(sFilename, fun):
        with open(sFilename, mode='r') as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                fun(line)
