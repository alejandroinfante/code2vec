#!/usr/bin/python

import multiprocessing
import os
import sys
import shutil
import subprocess
from threading import Timer
import sys
from argparse import ArgumentParser
from subprocess import Popen, PIPE, STDOUT, call

DB_PATH = ""
DATASET_ID = ""
CPU_CORES = ""
PHARO_IMAGE = ""
# PHARO_VM = '/data/ainfante/code2vec/PharoExtractor/pharo64-linux-stable/bin/pharo'
PHARO_VM = 'pharo64'

TMP_DIR = ""

def extractPathsFromDB(processId):
    command = [PHARO_VM, '--headless', PHARO_IMAGE, 'extractFromDB', DB_PATH, DATASET_ID, str(CPU_CORES), str(processId + 1) ]

    kill = lambda process: process.kill()
    outputFileName = TMP_DIR + str(processId)
    failed = False
    with open(outputFileName, 'a') as outputFile:
        sleeper = subprocess.Popen(command, stdout=outputFile, stderr=subprocess.PIPE)
        timer = Timer(600000, kill, [sleeper])

        try:
            timer.start()
            stdout, stderr = sleeper.communicate()
        finally:
            timer.cancel()

        if sleeper.poll() == 0:
            if len(stderr) > 0:
                print(sys.stderr, stderr, file=sys.stdout)
        else:
            print(sys.stderr, 'dir: ' + str(dir) + ' was not completed in time', file=sys.stdout)
            failed = True
    if failed:
        if os.path.exists(outputFileName):
            os.remove(outputFileName)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-pharoimage", "--pharoimage", dest="pharoimage", required=True)
    parser.add_argument("-db", "--db", dest="db", required=False)
    parser.add_argument("-dataset", "--dataset", dest="dataset", required=False)
    parser.add_argument("-cpus", "--cpus", dest="cpus", required=False)
    args = parser.parse_args()

    TMP_DIR = "./tmp/feature_extractor%d/" % (os.getpid())
    PHARO_IMAGE = args.pharoimage
    DB_PATH = args.db
    DATASET_ID = args.dataset
    CPU_CORES = int(args.cpus)
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    os.makedirs(TMP_DIR)
    try:
        p = multiprocessing.Pool(CPU_CORES)
        p.map(extractPathsFromDB, range(CPU_CORES))
        output_files = os.listdir(TMP_DIR)
        for f in output_files:
            os.system("cat %s/%s" % (TMP_DIR, f))
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)