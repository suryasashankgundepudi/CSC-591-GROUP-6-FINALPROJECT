import argparse
from site import sethelper
from num import NUM
from operations import *
from optimize import OPTIMIZE
from discrete import XPLN
import os

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

