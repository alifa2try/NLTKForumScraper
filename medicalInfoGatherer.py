from bs4 import BeautifulSoup
import requests
import messageCleaner
from string import ascii_lowercase
import logging

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
    logger.info(' Starting [getListofDiseases()]: Beginning to gather list of diseases\n')
    diseases = []
    baseUrl = 'http://www.mayoclinic.org/diseases-conditions/index?letter='

    for letter in ascii_lowercase:
        # TODO: Put some exception handling in here as it is highly risky incase one of the letters returns no results

        url = baseUrl + letter
        results = requests.get(url)
        soup = BeautifulSoup(results.content, 'html.parser')

        rawDiseases = soup.findAll(name = 'ol', attrs = {'class' : ''})

        rawDiseases = rawDiseases[0].findAll(name = "li")
        
        for rawDisease in rawDiseases:
            disease = rawDisease.get_text().strip()    
            diseases.append(disease)

    logger.info(' Completed [getListofDiseases()]: Finished gathered list of diseases\n')
    return diseases

def getListofSymptoms():
    logger.info('Starting [getListofSymptoms()]: Beginning to gather list of symptoms\n')
    symptoms = []
    baseUrl = 'http://www.healthline.com/directory/symptoms-'

    for letter in ascii_lowercase:
        # TODO: Put some exception handling in here as it is highly risky incase one of the letters returns no results

        url = baseUrl + letter
        results = requests.get(url)
        soup = BeautifulSoup(results.content, 'html.parser')

        rawSymptoms = soup.findAll(name = "ul",  attrs = {'class' : 'box-directory-list'})

        rawSymptoms = rawSymptoms[0].findAll(name = "li")

        for rawSymptom in rawSymptoms:
                symptoms.append(rawSymptom.get_text())

    logger.info(' Completed [getListofSymptoms()]: Finished gathered list of symptoms\n')
    return symptoms
