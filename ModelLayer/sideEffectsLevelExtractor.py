import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from ModelLayer.argumentExtractor import argumentExtractor
from ModelLayer import naturalLanguageWhiz
import logging 

logger = logging.getLogger(__name__)

''' This class contains all of the rules for detecting whether the side effects are present or not

'''

# Check for mention of inverter word + symptom
#def checkForMentionOfNoSymptoms(sentence, symptoms, drugs, argExtractor, dobj):

#    symtomStatements = ['side-effects', 'side effects', 'symptoms', 'symptom']
#    taggedSentence = ''

#    try:
#        taggedSentence = naturalLanguageWhiz.tag(sentence)
#        if len(taggedSentence) <= 0:
#            return
#    except:
#        logger.exception('Error when running checkForMentionOfNoSymptoms')
#        return
        
#    symptomMentioned = ''


#    # no need to tag sentence because we are not using the POS function at all
#    for idx, word in enumerate(taggedSentence):
#            inverterScore = argExtractor.getInverterScore(word[0], idx, sentence, symtomStatements)
#            # If inverterScore == 0 it means we have not match
#            # If inveterScore == 1 it means we have a match. This could mean we have a sie effect or symptom
#            # If inverterScore == -1 it means we have an inverter word. This could mean we don't have a side effect or symptom
#            if inverterScore == 0:
#                continue
#            if inverterScore == -1:
#                symptomMentioned = 'No side Effects'
#                break
#            if inverterScore == 1:
#                symptomMentioned = 'Side effects present'
#                break

#    if symptomMentioned != '':
#        sentence = (sentence.replace("'","\\'"))

#        insertSql = "INSERT INTO SideEffectsPresent (Sentence, SideEffectsStatus, Drug) VALUES (%s, %s, %s);" % ("'"+ sentence + "'", "'"+ symptomMentioned + "'", "'" + '' + "'")
#        dobj.insert(insertSql)


def checkForMentionOfNoSymptoms(sentence, symptoms, drugs, argExtractor, dbobj):

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

    if indexOfSymptomKeyWord == -1:
        return

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







