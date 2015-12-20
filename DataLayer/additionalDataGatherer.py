from configparser import SafeConfigParser

def gatherListOfContractions():

    fileLocation = 'Data/listOfContractions.ini'

    config = SafeConfigParser()
    config.read(fileLocation)

    listOfContractions = []

    for value in config.items('contractions'):
        listOfContractions.append(value)

    return listOfContractions


gatherListOfContractions()