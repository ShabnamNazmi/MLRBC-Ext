import os
import os.path
import random

from joblib import Parallel, delayed
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt
from sklearn.model_selection import train_test_split

from DataManagement import DataManage
import MLRBC
from config import *
# random.seed(SEED_NUMBER)

class averageTrack():

    def __init__(self, NumberOfExperiment):
        self.NumberOfExperiments = NumberOfExperiment

        self.aveTrack()
        self.saveAverage()
        # self.avePerformance()

    def aveTrack(self):
        datasetList = []  # np.array([])
        for exp in range(self.NumberOfExperiments):
            file_name = DATA_HEADER  + "_MLRBC_LearnTrack" + "_" + str(exp+1) + '.txt'
            completeName = os.path.join(RUN_RESULT_PATH, file_name)
            try:
                arraylist = np.array([])
                headerList = np.array([])
                ds = open(completeName, 'r')
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', file_name)
                raise
            else:
                headerList = ds.readline().rstrip('\n').split('\t')  # strip off first row
                for line in ds:
                    lineList = line.strip('\n').split('\t')
                    arraylist = [float(i) for i in lineList]
                    datasetList.append(arraylist)
                ds.close()

        # print(datasetList)
        a = [row[0] for row in datasetList]  # Iterations
        b = [row[1] for row in datasetList]  # macro population size
        c = [row[2] for row in datasetList]  # micro population size
        d = [row[3] for row in datasetList]  # Hamming loss
        e = [row[4] for row in datasetList]  # Accuracy
        f = [row[5] for row in datasetList]  # Generality
        g = [row[7] for row in datasetList]  # TP
        h = [row[8] for row in datasetList]  # TN
        j = [row[9] for row in datasetList]  # over-General accuracy

        self.IterNum = a[0:int(len(a) / self.NumberOfExperiments)]
        macroPopSize = []
        self.macroPopSize_ave = []
        for i in range(self.NumberOfExperiments):
            macroPopSize.append(
                (b[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        macroPopSize = np.sum(macroPopSize, axis=0)
        for x in macroPopSize:
            self.macroPopSize_ave.append(x / self.NumberOfExperiments)

        microPopSize = []
        self.microPopSize_ave = []
        for i in range(self.NumberOfExperiments):
            microPopSize.append(
                (c[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        microPopSize = np.sum(microPopSize, axis=0)
        for x in microPopSize:
            self.microPopSize_ave.append(x / self.NumberOfExperiments)

        if PLOT_SETTING[0]:
            plt.figure(1)
            plt.plot(self.IterNum, self.macroPopSize_ave, 'r-', label='MacroPopSize')
            plt.plot(self.IterNum, self.microPopSize_ave, 'b-', label='MicroPopSize')
            legend = plt.legend(loc='center', shadow=True, fontsize='large')
            plt.xlabel('Iteration')
            plt.ylim([0, 1])

        accuracyEstimate = []
        self.accuracyEstimate_ave = []
        for i in range(self.NumberOfExperiments):
            accuracyEstimate.append(
                (e[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        accuracyEstimate = np.sum(accuracyEstimate, axis=0)
        for x in accuracyEstimate:
            self.accuracyEstimate_ave.append(x / self.NumberOfExperiments)

        overGenAccuracy = []
        self.overGenAccuracy_ave = []
        for i in range(self.NumberOfExperiments):
            overGenAccuracy.append((j[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        overGenAccuracy = np.sum(overGenAccuracy, axis=0)
        for x in overGenAccuracy:
            self.overGenAccuracy_ave.append(x / self.NumberOfExperiments)

        if PLOT_SETTING[1]:
            plt.figure(2)
            plt.plot(self.IterNum, self.accuracyEstimate_ave, 'b-', label = 'Accuracy Estimate')
            plt.plot(self.IterNum, self.overGenAccuracy_ave, 'r-', label = 'Over-general Accuracy Estimate')
            legend = plt.legend(loc='center', shadow=True, fontsize='large')
            plt.xlabel('Iteration')
            plt.ylim([0, 1])

        hlossEstimate = []
        self.hlossEstimate_ave = []
        for i in range(self.NumberOfExperiments):
            hlossEstimate.append(
                (d[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        hlossEstimate = np.sum(hlossEstimate, axis=0)
        for x in hlossEstimate:
            self.hlossEstimate_ave.append(x / self.NumberOfExperiments)

        if PLOT_SETTING[2]:
            plt.figure(3)
            plt.plot(self.IterNum, self.hlossEstimate_ave, '-b', label = "Hamming loss")
            legend = plt.legend(loc='center', shadow=True, fontsize='large')
            plt.xlabel('Iteration')
            plt.ylim([0, 1])

        aveGenerality = []
        self.aveGenerality_ave = []
        for i in range(self.NumberOfExperiments):
            aveGenerality.append(
                (f[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        aveGenerality = np.sum(aveGenerality, axis=0)
        for x in aveGenerality:
            self.aveGenerality_ave.append(x / self.NumberOfExperiments)

        if PLOT_SETTING[3]:
            plt.figure(4)
            plt.plot(self.IterNum, self.aveGenerality_ave, 'b-', label='AveGenerality')
            legend = plt.legend(loc='center', shadow=True, fontsize='large')
            plt.xlabel('Iteration')
            plt.ylim([0, 1])

        TP = []
        self.tp_ave = []
        for i in range(self.NumberOfExperiments):
            TP.append((g[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        TP = np.sum(TP, axis=0)
        for x in TP:
            self.tp_ave.append(x / self.NumberOfExperiments)

        TN = []
        self.tn_ave = []
        for i in range(self.NumberOfExperiments):
            TN.append((h[i * int(len(a) / self.NumberOfExperiments):(i + 1) * int(len(a) / self.NumberOfExperiments)]))
        TN = np.sum(TN, axis=0)
        for x in TN:
            self.tn_ave.append(x / self.NumberOfExperiments)

        if PLOT_SETTING[4]:
            plt.figure(5)
            plt.plot(self.IterNum, self.tp_ave, 'b-', label='TP')
            plt.plot(self.IterNum, self.tn_ave, 'r-', label='TN')
            legend = plt.legend(loc='center', shadow=True, fontsize='small')
            plt.xlabel('Iteration')
            plt.ylim(bottom = 0.0)

        plt.show()

    def saveAverage(self):

        file_name = DATA_HEADER + "_MLRBC_AveTrack" + '.txt'
        completeName = os.path.join(RUN_RESULT_PATH, file_name)
        try:
            learnTrackOut = open(completeName, 'w')
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', completeName)
            raise
        else:
            learnTrackOut.write("Iteration\tMacroP\tMicroP\tHL\tAcc\tGen\ttp\ttn\tOverGenAcc\n")

        for i in range(len(self.IterNum)):
            trackString = str(self.IterNum[i]) + "\t" + str(self.macroPopSize_ave[i]) + "\t" + str(self.microPopSize_ave[i]) \
                          + "\t" + str("%.2f" % self.hlossEstimate_ave[i]) + "\t" + str("%.2f" % self.accuracyEstimate_ave[i]) + "\t" \
                          + str("%.2f" % self.aveGenerality_ave[i]) + "\t" + str("%.2f" % self.tp_ave[i]) + "\t" + str("%.2f" % self.tn_ave[i]) + "\t" + str("%.3f" % self.overGenAccuracy_ave[i]) + "\n"
            learnTrackOut.write(trackString)

        learnTrackOut.close()

    def avePerformance(self):
        n = 3
        performance = {}
        performanceList = []
        for exp in range(self.NumberOfExperiments):
            file_name = POP_STAT_HEADER + "_" + str(exp + 1) + '.txt'
            completeName = os.path.join(MAIN_RESULTS_PATH, POP_STAT_PATH, file_name)
            try:
                headerList = np.array([])
                f = open(completeName, 'r')
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open ', file_name)
                raise
            else:
                title = f.readline()
                headerList = f.readline().rstrip('\n').split('\t')  # strip off first row
                for i in range(n):
                    lineList = f.readline().strip('\n').split('\t')
                    perf = []
                    for p in lineList[1:]:
                        if p != 'NA':
                            perf.append(float(p))
                        else:
                            perf.append(0.0)
                    performance[lineList[0]] = perf
                f.close()
            performanceList.append(performance)

        avePerformance = dict.fromkeys(performanceList[0].keys(), np.array([0, 0]))
        for prf in performanceList:
            for key in prf.keys():
                array = np.array(prf[key])
                avePerformance[key] = avePerformance[key] + array

        for key in avePerformance.keys():
            avePerformance[key] = avePerformance[key] / self.NumberOfExperiments

        self.printPerformance(avePerformance)

    def printPerformance(self, avePerformance):
        print('Average training and test statistics:')
        print('\t\t\tTraining\tTest')
        for key in avePerformance.keys():
            temp = avePerformance.get(key)
            print(key + ': ' + "%.3f" % round(temp[0],3) + '\t' + "%.3f" % round(temp[1], 3))


class parallelRun():

    def __init__(self):
        self.defaultSplit = 0.7

    def doParallel(self):
        arg_instances = []
        if NUMBER_OF_FOLDS > 1:
            for it in range(NUMBER_OF_FOLDS):
                argument = []
                argument.append(it + 1)
                trainFileName = TRAIN_DATA_HEADER + "-" + str(it + 1) + ".txt"
                completeTrainFileName = os.path.join(DATA_FOLDER, DATA_HEADER, trainFileName)
                validFileName = VALID_DATA_HEADER + "-" + str(it + 1) + ".txt"
                completeValidFileName = os.path.join(DATA_FOLDER, DATA_HEADER, validFileName)
                dataManage = DataManage(completeTrainFileName, completeValidFileName)
                argument.append(dataManage)
                arg_instances.append(argument)
            Parallel(n_jobs = NO_PARALLEL_JOBS, verbose=1, backend="threading")(map(delayed(MLRBC.MLRBC), arg_instances))
        else:
            if (NO_EXPERIMENTS_AVERAGING > 1):
                completeTrainFileName = os.path.join(DATA_FOLDER, DATA_HEADER, TRAIN_DATA_HEADER + ".txt")
                completeValidFileName = os.path.join(DATA_FOLDER, DATA_HEADER, VALID_DATA_HEADER + ".txt")
                trainDataCSV = os.path.join(DATA_FOLDER, DATA_HEADER, TRAIN_DATA_HEADER + "-csv.csv")
                validDataCSV = os.path.join(DATA_FOLDER, DATA_HEADER, VALID_DATA_HEADER + "-csv.csv")
                completeDataFileName = os.path.join(DATA_FOLDER, DATA_HEADER, DATA_HEADER + "-csv.csv")

                if os.path.isfile(completeTrainFileName):      # training.txt exists
                    pass
                else:
                    if os.path.isfile(trainDataCSV):           # training.csv exists
                        convertCSV2TXT(trainDataCSV, completeTrainFileName)
                        convertCSV2TXT(validDataCSV, completeValidFileName)
                    elif os.path.isfile(completeDataFileName):        # no data split exists, searching for complete.csv
                        completeData = pd.read_csv(completeDataFileName)
                        completeDataSampled = self.tuneCard(completeData)
                        data_train, data_valid = train_test_split(completeDataSampled, test_size = 1 - self.defaultSplit,
                                                                     random_state = SEED_NUMBER)
                        data_train.to_csv(trainDataCSV)
                        data_valid.to_csv(validDataCSV)
                        convertCSV2TXT(os.path.join(DATA_FOLDER, DATA_HEADER, TRAIN_DATA_HEADER + "-csv.csv"), completeTrainFileName)
                        convertCSV2TXT(os.path.join(DATA_FOLDER, DATA_HEADER, VALID_DATA_HEADER + "-csv.csv"), completeValidFileName)
                dataManage = DataManage(completeTrainFileName, completeValidFileName, self.classCount, self.dataInfo)
                for it in range(NO_EXPERIMENTS_AVERAGING):
                    argument = []
                    argument.append(it + 1)
                    argument.append(dataManage)
                    argument.append(self.majLP)
                    argument.append(self.minLP)
                    arg_instances.append(argument)
                Parallel(n_jobs = NO_PARALLEL_JOBS, verbose = 1, backend = "multiprocessing")(map(delayed(MLRBC.MLRBC), arg_instances))
            else:
                completeTrainFileName = os.path.join(DATA_FOLDER, DATA_HEADER, TRAIN_DATA_HEADER + ".txt")
                completeValidFileName = os.path.join(DATA_FOLDER, DATA_HEADER, VALID_DATA_HEADER + ".txt")
                trainDataCSV = os.path.join(DATA_FOLDER, DATA_HEADER, TRAIN_DATA_HEADER + "-csv.csv")
                validDataCSV = os.path.join(DATA_FOLDER, DATA_HEADER, VALID_DATA_HEADER + "-csv.csv")
                completeDataFileName = os.path.join(DATA_FOLDER, DATA_HEADER, DATA_HEADER + "-csv.csv")

                if os.path.isfile(completeTrainFileName):      # training.txt exists
                    pass
                else:
                    if os.path.isfile(trainDataCSV):           # training.csv exists
                        convertCSV2TXT(trainDataCSV, completeTrainFileName)
                        convertCSV2TXT(validDataCSV, completeValidFileName)
                    elif os.path.isfile(completeDataFileName):        # no data split exists, searching for complete.csv
                        completeData = pd.read_csv(completeDataFileName)
                        completeDataSampled = self.tuneCard(completeData)
                        data_train, data_valid = train_test_split(completeDataSampled, test_size = 1 - self.defaultSplit,
                                                                     random_state = SEED_NUMBER)
                        data_train.to_csv(trainDataCSV)
                        data_valid.to_csv(validDataCSV)
                        convertCSV2TXT(os.path.join(DATA_FOLDER, DATA_HEADER, TRAIN_DATA_HEADER + "-csv.csv"), completeTrainFileName)
                        convertCSV2TXT(os.path.join(DATA_FOLDER, DATA_HEADER, VALID_DATA_HEADER + "-csv.csv"), completeValidFileName)
                dataManage = DataManage(completeTrainFileName, completeValidFileName, self.classCount, self.dataInfo)
                MLRBC.MLRBC([1, dataManage, self.majLP, self.minLP])

    def dataProp(self, infilename):
        """
        :param infilename: the complete dataset file in .csv format
        """
        try:
            df = pd.read_csv(infilename)
            Class = []  # list of all targets
            labelList = []
            classCount = {}
            for idx, row in df.iterrows():
                label = [int(l) for l in row[NO_ATTRIBUTES:]]
                newlabel = "".join(map(str, label))
                Class.append(newlabel)
                if newlabel in labelList:
                    classCount[newlabel] += 1
                else:
                    labelList.append(newlabel)
                    classCount[newlabel] = 1

            self.classCount = classCount
            print("dataProp: " + str(len(classCount)) + " unique LPs detected.")

            self.majLP = ""
            self.minLP = ""
            for key, value in classCount.items():
                if value == max(classCount.values()):
                    self.majLP = key
                if value == min(classCount.values()):
                    self.minLP = key
            # print("dataProp: " + "Majority LP: " + self.majLP + " and Minority LP: " + self.minLP)
            lpIR = max(classCount.values()) / min(classCount.values())

            classCount = len(Class[0])
            dataCount = len(Class)
            labelHeader = list(df.columns)
            dfCopy = df.copy()
            classHeader = labelHeader[NO_ATTRIBUTES:]
            dfCopy.drop(classHeader, axis=1, inplace = True)
            dfCopy["Class"] = Class
            data = dfCopy

            count = 0.0
            for rowIdx, row in data.iterrows():
                label = row["Class"]
                count += self.countLabel(label)
            card = count / dataCount
            dens = card / classCount

            Y = np.empty([classCount])
            for y in range(classCount):
                sampleCount = 0
                for rowIdx, row in data.iterrows():
                    label = row["Class"]
                    if label[y] == '1':
                        sampleCount += 1
                Y[y] = sampleCount

            IRLbl = np.empty([classCount])
            maxIR = Y.max()
            for it in range(classCount):
                IRLbl[it] = (maxIR/Y[it])
            meanIR = IRLbl.sum() / classCount

            temp = (IRLbl - meanIR)**2
            IRLbls = sqrt(temp.sum() / (classCount - 1))
            CVIR = IRLbls / meanIR

            self.dataInfo = dict(zip(["card", "dens", "LP-IR", "MaxIR", "MeanIR", "IRLbls", "CVIR"], [card, dens, lpIR, maxIR, meanIR, IRLbls, CVIR]))
            print("dataProp: " + str(self.dataInfo))
        except FileNotFoundError:
            print("completeData.csv not found.")

    def tuneCard(self, inData):
        """
        :param inData: complete data in pd format
        :return outData: down sampled data in pd format
        """
        if REF_CARDINALITY is None:
            outData = inData.copy()
            pass
        else:
            ClassDict = {}
            Class = []
            for idx, row in inData.iterrows():
                label = [int(l) for l in row[NO_ATTRIBUTES:]]
                newlabel = "".join(map(str, label))
                Class.append(newlabel)
                # if newlabel in ClassDict.keys():
                #     ClassDict[newlabel] += 1
                # else:
                #     ClassDict[newlabel] = 1
            labelHeader = list(inData.columns)
            outData = inData.copy()
            classHeader = labelHeader[NO_ATTRIBUTES:]
            outData.drop(classHeader, axis=1, inplace=True)
            outData["Class"] = Class
            outData.sample(frac = 1, random_state = SEED_NUMBER )    # ***Cool Command!***

            if self.dataInfo["card"] <= REF_CARDINALITY:
                print("tuneCard: Increasing the label cardinality by down-sampling...")
                theta_LP = int(REF_CARDINALITY)
                downsample_LPs = []
                class_unique = list(set(Class))     # ***Cool Command!***
                for lp in class_unique:
                    if self.countLabel(lp) <= theta_LP:
                        downsample_LPs.append(lp)
                        # downsample_LPs[lp] = ClassDict[lp]

                while self.card(outData) < REF_CARDINALITY:
                    "drop samples"
                    # dropLP = min(ClassDict, key=ClassDict.get)     # ***Cool Command!***
                    # if dropLP in downsample_LPs:
                    #     outData = outData[outData["Class"] != dropLP]
                    #     outData = outData.reset_index(drop = True)
                    # ClassDict.pop(dropLP, None)
                    for i in range(10):
                        random_row = random.randint(0, len(outData))
                        if outData.loc[random_row]["Class"] in downsample_LPs:
                             outData.drop([random_row], inplace = True, axis = 0)
                        outData = outData.reset_index(drop = True)
                print("The size of the down-sampled data is: " + str(len(outData)))
            else:
                print("tuneCard: Decreasing the label cardinality by down-sampling...")
                theta_LP = int(REF_CARDINALITY) + 1
                downsample_LPs = []
                class_unique = list(set(Class))
                for lp in class_unique:
                    if self.countLabel(lp) >= theta_LP:
                        downsample_LPs.append(lp)

                while self.card(outData) > REF_CARDINALITY:
                    "drop samples"
                    for i in range(10):
                        random_row = random.randint(0, len(outData)-1)
                        if outData.loc[random_row]["Class"] in downsample_LPs:
                            outData.drop([random_row], inplace = True, axis = 0)
                        outData = outData.reset_index(drop = True)
                print("The size of the down-sampled data is: " + str(len(outData)))

            listLabels = []
            for idx, row in outData.iterrows():
                listLabels.append(list(row["Class"]))
            outData.drop(["Class"], axis = 1, inplace = True)
            for l in range(len(listLabels[0])):
                outData["label" + str(l)] = [row[l] for row in listLabels]

        if DOWN_SAMPLE_RATIO < 1.0:
            sampleCount = round(len(outData) * DOWN_SAMPLE_RATIO)
            outData = outData.loc[0: sampleCount]

        return outData

    def card(self, data):
        """
        :return card: the multi-label class cardinality
        """
        count = 0.0
        for rowIdx, row in data.iterrows():
            label = row["Class"]
            count += self.countLabel(label)
        card = count / len(data)
        dens = card / len(label)

        return card

    def countLabel(self, label):
        count = 0
        for L in label:
            if float(L) != 0:
                count += 1
        return count

def convertCSV2TXT(infilename, outfilename):
    """
    :param infileName: input .csv file name
    :param outfilename: output .txt file name
    """

    try:
        df = pd.read_csv(infilename)
        df.drop(df.columns[0], axis=1, inplace=True)
        if "Class" in df:
            dfCopy = df.astype({"Class": str})
        else:
            Class = []
            for idx, row in df.iterrows():
                label = [int(l) for l in row[NO_ATTRIBUTES:]]
                newlabel = "".join(map(str, label))
                Class.append(newlabel)

            labelHeader = list(df.columns)
            dfCopy = df.copy()
            classHeader = labelHeader[NO_ATTRIBUTES:]
            dfCopy.drop(classHeader, axis=1, inplace = True)
            dfCopy["Class"] = Class

        data = dfCopy.values
        headerList = list(dfCopy.columns.values)
        Header = ''
        for it in range(len(headerList)-1):
            Header = Header + headerList[it] + '\t'
        Header = Header + headerList[-1]
        np.savetxt(outfilename, data, fmt = '%s', header = Header, delimiter = '\t', newline = '\n', comments='')
    except:
        pass



if __name__== "__main__":

    random.seed(SEED_NUMBER)
    parallel = parallelRun()

    completeDataFileName = os.path.join(DATA_FOLDER, DATA_HEADER, DATA_HEADER + "-csv.csv")
    parallel.dataProp(completeDataFileName)

    pathlib.Path(os.path.join(RUN_RESULT_PATH)).mkdir(parents=True, exist_ok=True)
    parallel.doParallel()

    if (DO_AVERAGING == True):
        averageTrack(NO_EXPERIMENTS_AVERAGING)