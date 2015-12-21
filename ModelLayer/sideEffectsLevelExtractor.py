import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from ModelLayer.argumentExtractor import argumentExtractor
from ModelLayer import naturalLanguageWhiz
from Utilities import messageCleaner
import logging 

logger = logging.getLogger(__name__)

''' This class contains all of the rules for detecting whether the side effects are present or not

'''


def checkSideEffectStatuses(sentence, argExtractor, dbobj):
    
    (noSymptomResult, noSymptomStatus) = checkForMentionOfNoSymptoms(sentence, argExtractor)

    (noInverterResult, noInverterStatus) = checkForInverterWordInPreceedingSentence(sentence, argExtractor)

    (symptomAndSideEffectMentioned, symptomAndSideEffectMentionedStatus) = checkIfSymptomAndSideEffectMentioned(sentence, argExtractor)

    '''Here are listed the order of preferance between the various hand coded rules
    '''

    if noSymptomResult:
        insertIntoDB(sentence, noSymptomStatus, dbobj)

    elif symptomAndSideEffectMentioned:
        insertIntoDB(sentence, symptomAndSideEffectMentionedStatus, dbobj)

    elif noInverterResult and not noSymptomResult:
        insertIntoDB(sentence, noInverterStatus, dbobj)
    
    elif (noSymptomStatus and not noSymptomResult):
        insertIntoDB(sentence, noSymptomStatus, dbobj)
    
    elif (noInverterStatus and not noInverterResult):
        insertIntoDB(sentence, noInverterStatus, dbobj)





def checkForMentionOfNoSymptoms(sentence, argExtractor):

    symtomStatements = ['side-effects', 'side effects', 'symptoms', 'symptom']

    # Extract the words preceeding the symptomStatement keyword
    preceedingSentence = ''
    symptomMentioned = ''

    for symptomStatement in symtomStatements:

        indexOfSymptomKeyWord = sentence.find(symptomStatement)

        if indexOfSymptomKeyWord == -1:
            continue

        # We pull out the preceeeding sentence. We have a -1 here in the final index range so that we can remove the space before the key symptom word
        preceedingSentence = sentence[0:(indexOfSymptomKeyWord - 1)]
        break

    # This means we could not find the key word from the side effects list
    if preceedingSentence == '':
        return (False, symptomMentioned)

    try:
        taggedSentence = naturalLanguageWhiz.tag(preceedingSentence)
        if len(taggedSentence) <= 0:
            return (False, symptomMentioned)
    except:
        logger.exception('Error when running checkForMentionOfNoSymptoms')
        return (False, symptomMentioned)

    result = argExtractor.checkIfInverterWordEndOfSentence(taggedSentence)

    if result == True:
        symptomMentioned = 'No Side Effects'
        return (True, symptomMentioned)
    else:
        symptomMentioned = 'Side effects Present - because of no direct inverter word before '
        return (False, symptomMentioned)

    


def checkForInverterWordInPreceedingSentence(sentence, argExtractor):

    #TODO: Work on an NLTK contractions aclass to filer out words like not etc 

    symtomStatements = ['side-effects', 'side effects', 'symptoms', 'symptom']

    # Extract the words preceeding the symptomStatement keyword
    preceedingSentence = ''
    sideEffectStatus = ''

    listOfContractions = argExtractor.getListOfContractions()
    expandedSentence = messageCleaner.replaceWordContractions(sentence, listOfContractions)

    for symptomStatement in symtomStatements:

        indexOfSymptomKeyWord = expandedSentence.find(symptomStatement)

        if indexOfSymptomKeyWord == -1:
            continue

        # We pull out the preceeeding sentence. We have a -1 here in the final index range so that we can remove the space before the key symptom word
        preceedingSentence = expandedSentence[0:(indexOfSymptomKeyWord - 1)]
        break

    # This means we could not find the key word from the side effects list
    if preceedingSentence == '':
        return (False, sideEffectStatus)

    try:
        taggedSentence = naturalLanguageWhiz.tag(preceedingSentence)
        if len(taggedSentence) <= 0:
            return (False, sideEffectStatus)
    except:
        logger.exception('Error when running checkForMentionOfNoSymptoms')
        return (False, sideEffectStatus)

    result = argExtractor.checkIfInverterWordInSentence(taggedSentence)

    if result == True:
        sideEffectStatus = 'Possibly no side effects'
        return (True, sideEffectStatus)
    else:
        sideEffectStatus = 'Side effects Present - because no preceeding inverterword'
        return (False, sideEffectStatus)


def checkIfSymptomAndSideEffectMentioned(sentence, argExtractor):
    symtomStatements = ['side-effects', 'side effects', 'symptoms', 'symptom']

    # Extract the words preceeding the symptomStatement keyword
    preceedingSentence = ''
    sideEffectStatus = ''
    sideEffectFound = False

    # TODO: Find out if it's useful to have contractions removed when looking for symtpoms
    listOfContractions = argExtractor.getListOfContractions()
    expandedSentence = messageCleaner.replaceWordContractions(sentence, listOfContractions)

    for symptomStatement in symtomStatements:

        indexOfSymptomKeyWord = expandedSentence.find(symptomStatement)

        if indexOfSymptomKeyWord == -1:
            continue
        
        else:
            sideEffectFound = True

    if not sideEffectFound:
        return (sideEffectFound, sideEffectStatus)

    listOfSymptoms = argExtractor.getListOfSymptoms()

    for symptom in listOfSymptoms:

        lowerCaseSymp = symptom.lower()
        if lowerCaseSymp in expandedSentence:
            sideEffectStatus = 'Side effects Present - because symptoms mentioned'
            return (sideEffectFound, sideEffectStatus)
        
    return (False, sideEffectStatus)


def insertIntoDB(sentence, category, dbobj):

    sqlSentence = (sentence.replace("'","\\'"))

    insertSql = "INSERT INTO SideEffectsPresent (Sentence, SideEffectsStatus, Drug) VALUES (%s, %s, %s);" % ("'"+ sqlSentence + "'", "'"+ category + "'", "'" + '' + "'")
    dbobj.insert(insertSql)





