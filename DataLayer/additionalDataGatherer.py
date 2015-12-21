from configparser import SafeConfigParser
from Utilities import messageCleaner

def getListOfContractions():

    fileLocation = 'Data/listOfContractions.ini'

    config = SafeConfigParser()
    config.read(fileLocation)

    listOfContractions = {}

    for (key, value) in config.items('contractions'):
        listOfContractions[key] = value
    
    return listOfContractions

def getListOfFromCSV(fileName):

    data = []

    with open(fileName, encoding = 'utf-8', errors = 'ignore') as f:
        data = f.readlines()
  
    list = []
    for member in data: 
        member = messageCleaner.removeSpecialCharacter(member)
        list.append(member)

    return list

