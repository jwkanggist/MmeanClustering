#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: clusteringWorker.py
#
# written by Jaewook Kang @ May 2017
#------------------------------------------------------------

from os import getcwd
import sys
sys.path.insert(0,getcwd()+'/data/')

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from datetime import date
import matplotlib.pyplot as matplot

class clusteringWorker(object):

    def __init__(self,datafilename):
        self.mNumOfCluster   = 10
        self.mNumofVector    = 22464
        self.mDimOfVector    = 32
        self.mNumOfIter      = 0
        self.mDataFileName = datafilename
        self.mDataFileDir  = getcwd() + self.mDataFileName
        self.mDataVectorLabel = [elem for elem in range(0,self.mDimOfVector)]
        self.mDataIndex       = [elem for elem in range(0,self.mNumofVector)]

        self.mDfMmean        = DataFrame(columns=self.mDataVectorLabel)

        self.mDfData         = DataFrame(columns=self.mDataVectorLabel)
        # self.mDfCluster      = DataFrame(index=self.mDataIndex)
        self.mDfCluster      = DataFrame()

        self.mSumOfSqrOfDist = []

        self.mExportFilenameForCluster = getcwd() + '/csvfiles/'+ str(date.today()) + '_ClusteringTrackResult.csv'
        self.mExportFilenameForMean = getcwd() + '/csvfiles/'+ str(date.today()) + '_MeanResult.csv'


    def exportCSVfiles(self):

        self.mDfMmean.to_csv(self.mExportFilenameForMean,encoding='utf-8')
        self.mDfCluster.to_csv(self.mExportFilenameForCluster,encoding='utf-8')


    def getEuclidianDist(self,vec1,vec2):
        diffvec = vec1 - vec2
        diffvec = np.square(diffvec)
        diffvec = np.sum(diffvec)
        return np.sqrt(diffvec)


    def initMmeanVectors(self):
        # use Forgy method which randomly chooses k data vectors for initial value of the mean
        initMeanIndex = np.random.choice(self.mNumofVector,self.mNumOfCluster,replace=False)
        # initMeanIndex = np.random.choice(500,self.mNumOfCluster,replace=False)

        print '# [ClusteringWorker] initMean is randomly selected from dataset'
        print '# [ClusteringWorker] whose data indices are : %s' % initMeanIndex
        for i in range(0,self.mNumOfCluster):
            self.mDfMmean.loc[i] = self.mDfData.loc[initMeanIndex[i]]




    def assigmentStep(self):
    # cal euclidian distance and choose the nearest cluster

        print '#=========== Iteration # %s ============' % self.mNumOfIter

        clusteringResult    = Series(index=self.mDataIndex)
        minDistList         = Series(index=self.mDataIndex)

        for i in range(0,self.mNumofVector):
        # for i in range(0, 500):

            distList = []
            for j in range(0,self.mNumOfCluster):
                tempdist = self.getEuclidianDist(self.mDfMmean.loc[j],self.mDfData.loc[i])
                distList.append(tempdist)

            minDistList.loc[i]      = min(distList)
            clusteringResult.loc[i] = np.argmin(distList)

        mDfClustLabel = [elem for elem in range(0,self.mNumOfIter+1)]

        self.mDfCluster =pd.concat([self.mDfCluster, clusteringResult],axis=1)
        self.mDfCluster.columns = mDfClustLabel
        self.mSumOfSqrOfDist.append(minDistList.sum())
        print '# [ClusteringWorker] Sum of Euclidian Distance from all data = %s' % self.mSumOfSqrOfDist[-1]


    def updateMean(self,dampingFactor):
        for i in range(0,self.mNumOfCluster):
            tempindex = self.mDfCluster[self.mDfCluster[self.mNumOfIter] == i ].index
            print '# [ClusteringWorker] # of data in the Cluster %s = %s' %( i, tempindex.size)

            if tempindex.size > 0:
                nextMean = self.mDfData.loc[tempindex].mean()
                self.mDfMmean.loc[i] =  (1 - dampingFactor) * self.mDfMmean.loc[i] + dampingFactor * nextMean
            else:
                if self.mNumOfIter < 5:
                    self.mDfMmean.loc[i] = np.random.choice(self.mNumofVector,1,replace=False)


        self.mNumOfIter += 1

    def readData(self):

        print '# [ClusteringWorker] The data loading from %s' % self.mDataFileDir
        temparray       = np.fromfile(self.mDataFileDir,dtype=np.float32)
        temparray       = np.reshape(temparray,(self.mNumofVector,self.mDimOfVector))
        self.mDfData    = DataFrame(data=temparray)

        print '# [ClusteringWorker] The dim of data vectors = %s' % self.mDimOfVector
        print '# [ClusteringWorker] The num of data vectors = %s' % self.mNumofVector
        print '# [ClusteringWorker] The size of data = %s bytes' % temparray.nbytes



    def intro(self):
        print '# ===================================================================== #'
        print '# Title: Qualcomm Programming Assignment: Problem # 3'
        print '# ================================================'
        print '# Support Python interpreter: python2.7.12 anaconda2-4.1.1'
        print '# '
        print '# Final update: 2017 May'
        print '# Contributors: Jaewook Kang (jwkang@soundl.ly)'
        print '# ===================================================================== #'



