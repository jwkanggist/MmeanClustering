#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: runclustering.py
#
# written by Jaewook Kang @ May 2017
#------------------------------------------------------------

from os import system

import sys

import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as matplot

import clusteringWorker

system ('clear')

datafilename = '/data/features_32dim_float_22464samples.data'


algoWorker = clusteringWorker.clusteringWorker(datafilename)
numiter = 15

algoWorker.intro()
algoWorker.readData()
algoWorker.initMmeanVectors()

for i in range(0,numiter):
    algoWorker.assigmentStep()
    algoWorker.updateMean(0.5)

algoWorker.exportCSVfiles()





