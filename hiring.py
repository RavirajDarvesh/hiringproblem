import csv
import random
import pprint
from Candidates import ImportCandidate
import itertools


# FinalData = {}
def passCandidate(data):
    print(data)
    return FinalData

def processRawData(rawCsvData=None):

    weightagePercentage         = 0.15
    weightageExperience         = 0.25
    weightageBacklog            = 0.1
    weightageLanguage           = 0.07
    weightageCertification      = 0.20
    weightageHobbie             = 0.05
    weightagePH                 = 0.12
    weightageLocation           = 0.06

    # experinceScore = 0.3*4
    # candidateScore = experinceScore + percentageScore - backlogScore
    columnHeader = rawCsvData[0]
    rows         = rawCsvData[1:]
    availableCandidateList = []
    data = {}
    candidatesList = []
    #ListData Store the FinalData to be returned from this function
    ListData = []
    ListData.append(columnHeader)

    for candidateDetails in rows:
        for i in range(0,len(candidateDetails)):
            data[columnHeader[i]] = candidateDetails[i]
        candidatesList.append(data)
        data = {}
    ListData.append(candidatesList)

    return ListData



def getPermutuations(data, range):
    combinaions = itertools.permutations(data, range)
    # print(list(combinaions))
    return combinaions

def sortTuple(data):
     sortedCandidateData = sorted(data, key=lambda x: x[-1])[::-1]
     highestScore = sortedCandidateData[0][-1]
     FittnessScore = 0
     for criteriaList in sortedCandidateData:
         if criteriaList[-1]==highestScore:
            FittnessScore = FittnessScore + 1
     return sortedCandidateData[0]+(FittnessScore,)

def getFittestFromSelf(candidate, criteriaPermutuation,):

    #Defined Weitage for the Criteria's Set for Selection
    weightagePercentage         = 0.15
    weightageExperience         = 0.25
    weightageBacklog            = 0.1
    weightageLanguage           = 0.07
    weightageCertification      = 0.20
    weightageHobbie             = 0.05
    weightagePH                 = 0.12
    weightageLocation           = 0.06
    tempCandidate = candidate
    for x in candidate:
        if x=='PERCENTAGE':
            if int(candidate[x])>=60:
                tempCandidate[x] = weightagePercentage
            else:
                tempCandidate[x] = 0
        if x=='BACKLOG':
            if int(candidate[x])==0:
                tempCandidate[x] = weightageBacklog
            else:
                tempCandidate[x] = 0
        if x=='LOCATION':
            if  candidate[x]:
                tempCandidate[x] = weightageLocation
            else:
                tempCandidate[x] = 0
        if x=='LANGUAGES':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageLanguage
            else:
                tempCandidate[x] = 0
        if x=='CERTIFICATION':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageCertification
            else:
                tempCandidate[x] = 0
        if x=='HOBBIES':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageHobbie
            else:
                tempCandidate[x] = 0
        if x=='PH':
            if candidate[x]=='NO':
                tempCandidate[x] = weightagePH
            else:
                tempCandidate[x] = 0
        if x=='EXPERIENCE':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageExperience
            else:
                tempCandidate[x] = 0
    tempcriteriaPermutuation = criteriaPermutuation
    print(tempcriteriaPermutuation)
    score = 0
    counter = 0
    for a in criteriaPermutuation:
        for b in a:
            if tempCandidate[b]:
                # print(b)
                score = score +tempCandidate[b]
                # print(score)
        tempcriteriaPermutuation[counter] += (score,)
        score = 0
        counter = counter + 1
    counter = 0
    # print(FittestModel)
    FittestModel = sortTuple(tempcriteriaPermutuation)
    return FittestModel


if __name__ == '__main__':
    candidates = ImportCandidate()
    rawCsvData = candidates.candidatesList()
    # print(candidatesList)
    processedData = processRawData(rawCsvData)
    availableCandidateList = processedData[1]
    availableCriteriaList  = processedData[0][2:]
    # print(availableCriteriaList)
    toleranceCriteria = int(input("There are %s Criteria in your Excel Sheet, Enter the minimum allowed Criteria: " %(len(availableCriteriaList))))

    #criteriaPermutuation holes the permutations of the critaria available using range defined by the user
    criteriaPermutuation = list(getPermutuations(availableCriteriaList, toleranceCriteria))
    FittestModel = []

    FittestModel.append(getFittestFromSelf(availableCandidateList[2], criteriaPermutuation))
    print(FittestModel)

    # for candidate in availableCandidateList:
    #     print(getFittestFromSelf(candidate, criteriaPermutuation))
