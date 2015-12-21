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
    
    (noSymptomResult, noSymptomStatus) = checkForMentionOfNoSymptoms(sentence, argExtractor, dbobj)

    (noInverterResult, noInverterStatus) = checkForInverterWordInPreceedingSentence(sentence, argExtractor, dbobj)

    if noSymptomResult and not noInverterResult:
        insertIntoDB(sentence, noSymptomStatus, dbobj)
    elif noSymptomResult and noInverterResult:
        insertIntoDB(sentence, noSymptomStatus, dbobj)
    elif noInverterResult and not noSymptomResult:
        insertIntoDB(sentence, noInverterStatus, dbobj)
    elif (noSymptomStatus and not noSymptomResult):
        insertIntoDB(sentence, noSymptomStatus, dbobj)
    elif (noInverterStatus and not noInverterResult):
        insertIntoDB(sentence, noInverterStatus, dbobj)





def checkForMentionOfNoSymptoms(sentence, argExtractor, dbobj):

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
            return
    except:
        logger.exception('Error when running checkForMentionOfNoSymptoms')
        return

    result = argExtractor.checkIfInverterWordEndOfSentence(taggedSentence)

    if result == True:
        symptomMentioned = 'No Side Effects'
        return (True, symptomMentioned)
    else:
        symptomMentioned = 'Side effects Present'
        return (False, symptomMentioned)

    


def checkForInverterWordInPreceedingSentence(sentence, argExtractor, dbobj):

    #TODO: Work on an NLTK contractions aclass to filer out words like not etc 

    symtomStatements = ['side-effects', 'side effects', 'symptoms', 'symptom']

    # Extract the words preceeding the symptomStatement keyword
    preceedingSentence = ''
    symptomMentioned = ''

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
        return (False, symptomMentioned)

    try:
        taggedSentence = naturalLanguageWhiz.tag(preceedingSentence)
        if len(taggedSentence) <= 0:
            return
    except:
        logger.exception('Error when running checkForMentionOfNoSymptoms')
        return

    result = argExtractor.checkIfInverterWordInSentence(taggedSentence)

    if result == True:
        symptomMentioned = 'Possibly no side effects'
        return (True, symptomMentioned)
    else:
        symptomMentioned = 'Side effects Present'
        return (False, symptomMentioned)


def insertIntoDB(sentence, category, dbobj):

    sqlSentence = (sentence.replace("'","\\'"))

    insertSql = "INSERT INTO SideEffectsPresent (Sentence, SideEffectsStatus, Drug) VALUES (%s, %s, %s);" % ("'"+ sqlSentence + "'", "'"+ category + "'", "'" + '' + "'")
    dbobj.insert(insertSql)




