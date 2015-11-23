from bs4 import BeautifulSoup
import requests
import messageCleaner
from string import ascii_lowercase
import logging
import csv
import os.path

logger = logging.getLogger(__name__)

# This script pulls togethor a list of diseases and symptoms

def getListofDiseasesWiki():
    diseases = []
    url= 'https://en.wikipedia.org/wiki/List_of_cancer_types'
    results = requests.get(url)
    soup = BeautifulSoup(results.content, 'html.parser')

    rawList = soup.find_all(name = "li")

    for item in rawList:
        diseases.append(item.get_text())

    return diseases 

def getListofDiseases():
    logger.info('Starting [getListofDiseases()]: Beginning to gather list of diseases')
    diseases = []
    baseUrl = 'http://www.mayoclinic.org/diseases-conditions/index?letter='
    fileName = 'listOfDiseases.csv'

    fileExists = os.path.isfile(fileName)

    if(fileExists):
        diseases = __getMedicalInfoListFromCSV(fileName)

    else:
        with open(fileName, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')

            for letter in ascii_lowercase:
                # TODO: Put some exception handling in here as it is highly risky incase one of the letters returns no results

                url = baseUrl + letter
                results = requests.get(url)
                soup = BeautifulSoup(results.content, 'html.parser')

                rawDiseases = soup.findAll(name = 'ol', attrs = {'class' : ''})

                rawDiseases = rawDiseases[0].findAll(name = "li")
            
                __writeMedicalInfoToCSV(f, writer, rawDiseases, diseases)
                #for rawDisease in rawDiseases:
                #    disease = rawDisease.get_text().strip()    
                #    diseases.append(disease)

    logger.info('Completed [getListofDiseases()]: Finished gathered list of diseases')
    return diseases

def getListofSymptoms():
    logger.info('Starting [getListofSymptoms()]: Beginning to gather list of symptoms')
    symptoms = []
    baseUrl = 'http://www.healthline.com/directory/symptoms-'
    fileName = 'listOfSymptoms.csv'

    fileExists = os.path.isfile(fileName)

    if(fileExists):
        symptoms = __getMedicalInfoListFromCSV(fileName)
    
    else:
        with open(fileName, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')

            for letter in ascii_lowercase:
                # TODO: Put some exception handling in here as it is highly risky incase one of the letters returns no results

                url = baseUrl + letter
                results = requests.get(url)
                soup = BeautifulSoup(results.content, 'html.parser')

                rawSymptoms = soup.findAll(name = "ul",  attrs = {'class' : 'box-directory-list'})

                rawSymptoms = rawSymptoms[0].findAll(name = "li")

                __writeMedicalInfoToCSV(f, writer, rawSymptoms, symptoms)
                #for rawSymptom in rawSymptoms:
                #        symptoms.append(rawSymptom.get_text())

    logger.info('Completed [getListofSymptoms()]: Finished gathered list of symptoms')
    return symptoms

def __getMedicalInfoListFromCSV(fileName):

    medicalInfoList = []

    with open(fileName, 'rt', encoding = 'utf8', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            medicalInfoList.append(row[0])
    
    return medicalInfoList

def __writeMedicalInfoToCSV(fileObj, writer, rawmedicalInfoList, medicalInfoList):

    for info in rawmedicalInfoList:
        writer.writerow([info.get_text().strip()])
        medicalInfoList.append(info.get_text().strip())
        fileObj.flush()
    
    return True
