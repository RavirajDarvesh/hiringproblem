import random
import pprint
from Candidates import ImportCandidate
import itertools

def processRawData(rawCsvData=None):
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
    score = 0
    # candidateScore =
    for x in candidate:
        if x=='PERCENTAGE':
            if int(candidate[x])>=60:
                tempCandidate[x] = weightagePercentage
                score = score + weightagePercentage
            else:
                tempCandidate[x] = 0
        if x=='BACKLOG':
            if int(candidate[x])==0:
                tempCandidate[x] = weightageBacklog
                score = score + weightageBacklog
            else:
                tempCandidate[x] = 0
        if x=='LOCATION':
            if  candidate[x]:
                tempCandidate[x] = weightageLocation
                score = score + weightageLocation
            else:
                tempCandidate[x] = 0
        if x=='LANGUAGES':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageLanguage
                score = score + weightageLanguage
            else:
                tempCandidate[x] = 0
        if x=='CERTIFICATION':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageCertification
                score = score + weightageCertification
            else:
                tempCandidate[x] = 0
        if x=='HOBBIES':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageHobbie
                score = score + weightageHobbie
            else:
                tempCandidate[x] = 0
        if x=='PH':
            if candidate[x]=='NO':
                tempCandidate[x] = weightagePH
                score = score + weightagePH
            else:
                tempCandidate[x] = 0
        if x=='EXPERIENCE':
            if int(candidate[x])>0:
                tempCandidate[x] = weightageExperience
                score = score + weightageExperience
            else:
                tempCandidate[x] = 0
    candidateScore = tempCandidate
    candidateScore['score'] = score
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

#Function to choose a candidate from a List without repetation
# def choice_without_repetition(lst):
#     i = 0
#     while True:
#         i = (i + random.randrange(1, len(lst))) % len(lst)
#         yield lst[i]

def getFinalScore(candidates):
    score = 0
    for candidate in candidates:
        if candidate['score']:
            score = score + float(candidate['score'])
    return score

if __name__ == '__main__':
    candidates = ImportCandidate()
    rawCsvData = candidates.candidatesList()
    # print(candidatesList)
    processedData = processRawData(rawCsvData)
    availableCandidateList = processedData[1]
    availableCriteriaList  = processedData[0][2:]
    print(type(availableCriteriaList))
    toleranceCriteria = int(input("There are %s Criteria in your Excel Sheet, Enter the minimum allowed Criteria: " %(len(availableCriteriaList))))
    numberOfCandidateRequired = int(input("How many candidates you are looking for?\n:"))
    minimumCandidatePopulation = numberOfCandidateRequired + 3

    #Assign Key "IsEligible" to available candidate list, so that it can  hold value for their Eligibility.
    for candidate in availableCandidateList:
        eligibilty = checkEligibilty(assignWeight(candidate, availableCriteriaList), toleranceCriteria)
        if eligibilty==True:
            candidate['isEligible'] = True
        else:
            candidate['isEligible'] = False
    IsEligibleCandidate = []
    for number in range(len(availableCandidateList)):
        if availableCandidateList[number]['isEligible']:
            IsEligibleCandidate.append(availableCandidateList[number])
    # pprint.pprint(len(IsEligibleCandidate))


    #Select Random Population for sorting from the given list if IsEligibleCandidate
    FinalSortedCandidates = []
    FinalSortingScore = 0
    while len(IsEligibleCandidate)>=minimumCandidatePopulation:
        data = random.sample(IsEligibleCandidate,numberOfCandidateRequired)
        for candidate in data:
            for tempCandidate in IsEligibleCandidate:
                if candidate['ID']==tempCandidate['ID']:
                    IsEligibleCandidate.remove(tempCandidate)
        SelectedCandidatesScore = getFinalScore(data)
        if SelectedCandidatesScore > FinalSortingScore:
            FinalSortedCandidates = data
            FinalSortingScore  = SelectedCandidatesScore

        print("Next Hello ---------------------------------//------------------------")

    pprint.pprint(data)
    print(FinalSortingScore)

    # pprint.pprint(IsEligibleCandidate)
    # print(len(data))
    # pprint.pprint(data)
