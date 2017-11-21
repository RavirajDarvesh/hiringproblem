import random
# import pprint
from Candidates import ImportCandidate
from operator import itemgetter
import csv


def processRawData(rawCsvData=None):
    columnHeader = rawCsvData[0]
    rows = rawCsvData[1:]
    data = {}
    candidatesList = []
    ListData = []
    ListData.append(columnHeader)

    for candidateDetails in rows:
        for i in range(0, len(candidateDetails)):
            data[columnHeader[i]] = candidateDetails[i]
        candidatesList.append(data)
        data = {}
    ListData.append(candidatesList)

    return ListData


def assignWeight(candidate, availableCriteriaList):
    weightagePercentage = 0.15
    weightageExperience = 0.25
    weightageBacklog = 0.1
    weightageLanguage = 0.07
    weightageCertification = 0.20
    weightageHobbie = 0.05
    weightagePH = 0.12
    weightageLocation = 0.06
    tempCandidate = candidate
    score = 0
    for x in candidate:
        if x == 'PERCENTAGE':
            if int(candidate[x]) >= 60:
                tempCandidate[x] = weightagePercentage
                score = score + weightagePercentage
            else:
                tempCandidate[x] = 0
        if x == 'BACKLOG':
            if int(candidate[x]) == 0:
                tempCandidate[x] = weightageBacklog
                score = score + weightageBacklog
            else:
                tempCandidate[x] = 0
        if x == 'LOCATION':
            if candidate[x]:
                tempCandidate[x] = weightageLocation
                score = score + weightageLocation
            else:
                tempCandidate[x] = 0
        if x == 'LANGUAGES':
            if int(candidate[x]) > 0:
                tempCandidate[x] = weightageLanguage
                score = score + weightageLanguage
            else:
                tempCandidate[x] = 0
        if x == 'CERTIFICATION':
            if int(candidate[x]) > 0:
                tempCandidate[x] = weightageCertification
                score = score + weightageCertification
            else:
                tempCandidate[x] = 0
        if x == 'HOBBIES':
            if int(candidate[x]) > 0:
                tempCandidate[x] = weightageHobbie
                score = score + weightageHobbie
            else:
                tempCandidate[x] = 0
        if x == 'PH':
            if candidate[x] == 'NO':
                tempCandidate[x] = weightagePH
                score = score + weightagePH
            else:
                tempCandidate[x] = 0
        if x == 'EXPERIENCE':
            if int(candidate[x]) > 0:
                tempCandidate[x] = weightageExperience
                score = score + weightageExperience
            else:
                tempCandidate[x] = 0
    candidateScore = tempCandidate
    candidateScore['SCORE'] = score
    tempCandidate = []
    return candidateScore


def checkEligibilty(candidateScore, tolerance):
    tolerance = tolerance + 2
    FinalData = {k: v for k, v in candidateScore.items() if v}
    checkData = 0
    for a in FinalData:
        checkData = checkData + 1

    if checkData >= tolerance:
        status = True
    else:
        status = False
    return status


def getSortedFinalCandidateList(candidates, numberOfCandidateRequired):
    # pprint.pprint(candidates)
    sortedCandidatesList = sorted(candidates, key=itemgetter('SCORE'),
                                  reverse=True)
    # pprint.pprint(sortedCandidatesList)
    return sortedCandidatesList[:numberOfCandidateRequired]


def getFinalScore(candidates):
    score = 0
    for candidate in candidates:
        if candidate['SCORE']:
            score = score + float(candidate['SCORE'])
    return score


def writeToCsv(csv_file_path, dict_data):
    csv_file = open(csv_file_path, 'w', encoding='utf8', newline='')
    writer = csv.writer(csv_file)
    # Seleting only required fields in the final csv five
    headers = ['ID', 'NAME', 'SCORE']
    writer.writerow(headers)

    for dat in dict_data:
        line = []
        for field in headers:
            line.append(dat[field])
        writer.writerow(line)
    csv_file.close()


if __name__ == '__main__':
    candidates = ImportCandidate()
    rawCsvData = candidates.candidatesList()
    processedData = processRawData(rawCsvData)
    availableCandidateList = processedData[1]
    availableCriteriaList = processedData[0][2:]
    toleranceCriteria = int(input(
        "There are %s Criteria in your Excel Sheet, Enter the minimum allowed Criteria: " % (len(availableCriteriaList))))
    numberOfCandidateRequired = int(
        input("How many candidates you are looking for?\n:"))
    minimumCandidatePopulation = numberOfCandidateRequired + 4

    # Assign Key "IsEligible" to available candidate list, so that it can  hold value for their Eligibility.
    for candidate in availableCandidateList:
        eligibilty = checkEligibilty(assignWeight(
            candidate, availableCriteriaList), toleranceCriteria)
        if eligibilty == True:
            candidate['ISELIGIBLE'] = True
        else:
            candidate['ISELIGIBLE'] = False
    IsEligibleCandidate = []
    for number in range(len(availableCandidateList)):
        if availableCandidateList[number]['ISELIGIBLE']:
            IsEligibleCandidate.append(availableCandidateList[number])

    # Select Random Population for sorting from the given list if IsEligibleCandidate
    FinalSortedCandidates = []
    FinalSortingScore = 0

    # Loop for seleccting random candidate populaton only THree times
    for a in range(3):
        if len(IsEligibleCandidate) >= minimumCandidatePopulation:
            # Random function to select random candidates from Eligible candidates list
            data = random.sample(IsEligibleCandidate,
                                 minimumCandidatePopulation)

            # For loop to remove the candidates currently selected in random list so that they do not get repeated in next iteration
            for candidate in data:
                for tempCandidate in IsEligibleCandidate:
                    if candidate['ID'] == tempCandidate['ID']:
                        IsEligibleCandidate.remove(tempCandidate)

            # Function to get the N number of Sorted list of candidates from the randomly selected candidates list, where N is the nnumber of candidates required by the user
            SelectedCandidates = getSortedFinalCandidateList(
                data, numberOfCandidateRequired)

            # Function to get Finalscore of the Selected Candidate so that it can be compared with the previous hired candidates to check for eligiblity
            SelectedCandidatesScore = getFinalScore(SelectedCandidates)
            if SelectedCandidatesScore > FinalSortingScore:
                FinalSortedCandidates = SelectedCandidates
                FinalSortingScore = SelectedCandidatesScore

    if FinalSortedCandidates == []:
        print("############ Attention Please ############")
        print("Provided Candidate List is too small for analysis, Kindly insert more data into the List \n OR try to sort with less criteria and Number of candidate required number")
    else:
        print("//-----------------------------------------Candidates Sorted Succesfully---------------------------------------------//")
        # for hiredCandidates in FinalSortedCandidates:
        #     print("Name : "+hiredCandidates['NAME']+"      Finalscore = "+str(round(hiredCandidates['SCORE'],2)))
        # print("Total Score of Currently Hired Candidates: "+ str(round(FinalSortingScore, 2)))
        # pprint.pprint(FinalSortedCandidates)

        print("Kindly check SelectedCandidates.csv file to get you results")
        writeToCsv('SelectedCandidates.csv', FinalSortedCandidates)
