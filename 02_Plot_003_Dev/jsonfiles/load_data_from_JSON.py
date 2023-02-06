# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 21:24:26 2021

@author: pobe4699
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 14:11:44 2021

@author: pobe4699
"""
annotatorTags = ["4DCARE_PO"]#,"FDC_PO"]  # "4DCARE_PO", "4DCARE_MG"]

from libs.load_json_func import *

#def load_Json_file():
data = loadDataFile("input/study-tags-"+annotatorTags[0][-2:]+".json")
#data = loadDataFile("input/study-tags-MG.json")
# for key in data:
#     print (key)
#
# for item in data.items():
#     print(item)

print(f"total cases are {len(data)}, the numebr of cases from "+annotatorTags[0]+" json file has been loaded...")
#print(len(data))
#print(json.dumps(data["study_id"], indent=2))

#annotatorTags = ["FDC_MG","FDC_PO"]
studyIds = extractStudyIdsForTags(annotatorTags, data)
print(f"Found {len(studyIds)} matching study OIDs for {annotatorTags}")

studyData = loadDataFile("input/studies-"+annotatorTags[0][-2:]+".json") #load the file ended with the initials of the first tag
matchingData = findStilIdsMatchingStudyIds(studyData, studyIds)
print(f"Found {len(matchingData)} matching STIL Ids for study OIDs")

#workspaces=loadDataFile("input/workspaces-" + annotatorTags[1][-2:] + ".json")

if len(annotatorTags)==1:
    userWiseMeasurementData = {}
    userWiseMeasurementData[annotatorTags[0]] = getMeasurements(
                                            loadDataFile("input/workspaces-"+annotatorTags[0][-2:]+".json"),
                                            matchingData)

    mergedMeasurements = mergeMeasurements1U(userWiseMeasurementData)
    addName_to_file=annotatorTags[0][-2:]

if len(annotatorTags)==2:
    userWiseMeasurementData = {}
    userWiseMeasurementData[annotatorTags[0]] = getMeasurements(
                                            loadDataFile("input/workspaces-"+annotatorTags[0][-2:]+".json"),
                                            matchingData)
    userWiseMeasurementData[annotatorTags[1]] = getMeasurements(
                                            loadDataFile("input/workspaces-"+annotatorTags[1][-2:]+".json"),
                                            matchingData)
    #
    mergedMeasurements = mergeMeasurements(userWiseMeasurementData)
    addName_to_file=annotatorTags[0][-2:]+"_"+annotatorTags[1][-2:]

measurementsFilename = "measurements.csv"


import time
timestr = time.strftime("%Y%m%d_%H_"+addName_to_file)
#print(f"{timestr}_Saving measurements to {measurementsFilename} ", end='')
saveMeasurementsToCSVFile(timestr+"_"+measurementsFilename, mergedMeasurements)
print("Saving measurements to the CSV file is finalised")


#if __name__ == "__main__":
#    load_Json_file()
