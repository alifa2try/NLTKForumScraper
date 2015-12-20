import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from ModelLayer.argumentExtractor import argumentExtractor
from ModelLayer import naturalLanguageWhiz
import logging 

logger = logging.getLogger(__name__)

''' This class contains all of the rules for detecting whether the side effects are present or not

'''

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
    else:
        symptomMentioned = 'Side effects Present'

    if symptomMentioned != '':
        sentence = (sentence.replace("'","\\'"))

        insertSql = "INSERT INTO SideEffectsPresent (Sentence, SideEffectsStatus, Drug) VALUES (%s, %s, %s);" % ("'"+ sentence + "'", "'"+ symptomMentioned + "'", "'" + '' + "'")
        dbobj.insert(insertSql)

def checkForInverterWordInPreceedingSentence(sentence, argExtractor, dbobj):

    #TODO: Work on an NLTK contractions aclass to filer out words like not etc 

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

    try:
        taggedSentence = naturalLanguageWhiz.tag(preceedingSentence)
        if len(taggedSentence) <= 0:
            return
    except:
        logger.exception('Error when running checkForMentionOfNoSymptoms')
        return

    result = argExtractor.checkIfInverterWordInSentence(taggedSentence)

    if result == True:
        symptomMentioned = 'Possibly No Side Effects'
    else:
        symptomMentioned = 'Side effects Present'

    if symptomMentioned != '':
        sentence = (sentence.replace("'","\\'"))

        insertSql = "INSERT INTO SideEffectsPresent (Sentence, SideEffectsStatus, Drug) VALUES (%s, %s, %s);" % ("'"+ sentence + "'", "'"+ symptomMentioned + "'", "'" + '' + "'")
        dbobj.insert(insertSql)

def checkForNegativeWordInProceedgingSentence(sentence, argExtractor, dbobj):

    # TODO: The next few lines were we pull out the sentence is a strong candidate for refactoring
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

    try:
        taggedSentence = naturalLanguageWhiz.tag(preceedingSentence)
        if len(taggedSentence) <= 0:
            return
    except:
        logger.exception('Error when running checkForMentionOfNoSymptoms')
        return














