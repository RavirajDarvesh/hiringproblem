import random
import pprint
from Candidates import ImportCandidate
import itertools
import pprint

def processRawData(rawCsvData=None):
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

def assignWeight(candidate,availableCriteriaList):
    weightagePercentage         = 0.15
    weightageExperience         = 0.25
    weightageBacklog            = 0.1
    weightageLanguage           = 0.07
    weightageCertification      = 0.20
    weightageHobbie             = 0.05
    weightagePH                 = 0.12
    weightageLocation           = 0.06
    tempCandidate = candidate
    # print(candidate)
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
    candidateScore = tempCandidate
    tempCandidate = []
    return candidateScore

def checkEligibilty(candidateScore, tolerance):
    tolerance = tolerance + 2
    tempCandidateScore = candidateScore
    FinalData = { k:v for k, v in candidateScore.items() if v }
    checkData = 0
    for a in FinalData:
        checkData = checkData + 1

    if checkData >= tolerance:
        status = True
    else:
        status = False
    return status




if __name__ == '__main__':
    candidates = ImportCandidate()
    rawCsvData = candidates.candidatesList()
    # print(candidatesList)
    processedData = processRawData(rawCsvData)
    availableCandidateList = processedData[1]
    availableCriteriaList  = processedData[0][2:]
    # print(availableCriteriaList)
    toleranceCriteria = int(input("There are %s Criteria in your Excel Sheet, Enter the minimum allowed Criteria: " %(len(availableCriteriaList))))
    eligible
    for candidate in availableCandidateList:
        print(candidate['ID']," ",checkEligibilty(assignWeight(candidate, availableCriteriaList), toleranceCriteria))
