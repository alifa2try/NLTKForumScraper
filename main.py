import nltk  
from DataLayer import medicalInfoGatherer
from DataLayer import postsGatherer
from DataLayer import forum
import logging
from ViewLayer import displayArguments
from ModelLayer.argumentExtractor import argumentExtractor
from Utilities import messageCleaner
from ModelLayer import naturalLanguageWhiz
from ModelLayer.sideEffectsLevelExtractor import sideEffectsLevelExtractor
from DataLayer.dataBaseConnector import dataBaseConnector
from DataLayer import additionalDataGatherer
from ModelLayer.symptomConditionExtractor import symptomConditionExtractor
from ModelLayer.experienceExtractor import experienceExtractor
from ModelLayer.supplementaryDrugExtractor import supplementaryDrugExtractor
from DataLayer import argumentInserter

def buildArgExtractorWithDataLists():
    logging.info('Starting [main]: Building data lists')

    listOfDiseases = medicalInfoGatherer.getListofDiseases()
    listOfSymptoms = medicalInfoGatherer.getListofSymptoms()
    listOfDrugs = medicalInfoGatherer.getListofDrugs()

    posWords = 'Data/positive-words.txt'
    negWords = 'Data/negative-words.txt'
    invWords = 'Data/inverter-words.txt'

    posList = additionalDataGatherer.getListOfFromCSV(posWords)
    negList = additionalDataGatherer.getListOfFromCSV(negWords)
    invList = additionalDataGatherer.getListOfFromCSV(invWords)
    contractionsList = additionalDataGatherer.getListOfContractions()

    logging.info('Finished [main]: Finished building data lists')
    
    argExtractor = argumentExtractor(listOfSymptoms, listOfDiseases, listOfDrugs, invList, posList, negList, contractionsList)

    return argExtractor

def main():
    logging.basicConfig(filename='log.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    # Gather the posts from all of the forums and the list of necessary medical terms 

    logging.info('-------------------------------------------------------')
    logging.info('-------------Starting Argument Extractor---------------')
    logging.info('-------------------------------------------------------')
    
    argExtractor = buildArgExtractorWithDataLists()

    forums = postsGatherer.gatherForums()
    dbobj = dataBaseConnector('DBConnector.ini')
    postCount = 0
    forumCount = 0
    # Loop through each of the forum posts and print the arguments onto the page. The arguments for and against each of the posts.
    # Some sort of extremley Naive Bayesian classifier 

    for forum in forums:
        posts = forum.getPosts()
        mainDrug = forum.getTreatment()
        postCount = postCount + len(posts)
        forumCount = forumCount + 1

        logging.info('Starting [main]: Beginning to search for symptoms and diseases within the posts')

        for post in posts:
            sentences = nltk.sent_tokenize(post.getReview())

            postWordScore = 0

            for sentence in sentences:

                sentenceScore = argExtractor.calculateWordScore(sentence)
                postWordScore = postWordScore + sentenceScore

                drugsFound = argExtractor.checkForDrugs(sentence)
                if len(drugsFound) > 0:
                    for drugFound in drugsFound:
                        if drugFound.lower() not in post.getDrugs():
                            post.setDrugs(drugFound.lower())

                # Make sure that we do not append a symptom twice.It may be the case that the post mentions a symptom twice in two or more sentences
                symptomsFound , reliefsFound = argExtractor.checkForSymptomInClause(sentence)
                if(len(symptomsFound) > 0):
                    for symptomFound in symptomsFound:
                        if symptomFound not in post.getSymptoms():
                            post.setSymptoms(symptomFound)
                
                foundDisease , disease = argExtractor.checkForDiseaseInClause(sentence)
                if(foundDisease and disease not in post.getDisease()):
                    post.setDisease(disease)

                symDrugRelations = argExtractor.checkdrugSymptomRelation(symptomsFound, drugsFound, sentence)
                if(len(symDrugRelations) > 0):
                    for symDrugRelation in symDrugRelations:
                        post.setSymptomDrugRelation(symDrugRelation)

                nounPhrases = naturalLanguageWhiz.extractNounPhrases(sentence)
                if(len(nounPhrases) > 0):
                    for nounPhrase in nounPhrases:
                        post.setNounPhrase(nounPhrase)
                        message = post.getReview()
                        sqlSentence = sentence.replace("'","\\'")

                        insertSql = "INSERT INTO ForumPostFeatures (Post, Sentence, nounPhrase) VALUES (%s, %s, %s);" 
                        data = (message, sqlSentence, nounPhrase.lower())
                        dbobj.insert(insertSql, data)
                
                # Construct argument rules newly here so that objects are fresh and can store fresh data each iteration
                sideEffectsLevelExtractorObj = sideEffectsLevelExtractor()
                experienceExtractorObj = experienceExtractor()
                symptomConditionExtractorObj = symptomConditionExtractor()
                supplementaryDrugExtractorObj = supplementaryDrugExtractor()

                # These are all the argument set extraction rules
                naturalLanguageWhiz.extractConnectingVerbs(sentence.lower(), symptomsFound, drugsFound, dbobj)
                sideEffectsLevelExtractorObj.checkSideEffectStatuses(sentence.lower(), argExtractor, forum.getTreatment(), dbobj)
                symptomConditionExtractorObj.checkSymptomConditions(sentence.lower(), sentenceScore, symptomsFound, forum.getTreatment(), argExtractor, dbobj)
                experienceExtractorObj.checkForMentionOfSentimentOnly(sentence, sentenceScore, symptomsFound, drugsFound, forum.getTreatment(), argExtractor, dbobj)
                supplementaryDrugExtractorObj.findSupplementaryDrug(sentence, mainDrug, drugsFound, symptomsFound, dbobj)

                # Insert into the DB
                argumentInserter.insertArgumentSetsIntoDB(post, sideEffectsLevelExtractorObj, experienceExtractorObj, symptomConditionExtractorObj, supplementaryDrugExtractorObj, dbobj)

                # TODO: Move this ASAP. This checks to see if symptoms have worsened or not
                if (sentenceScore != 0) and (len(nounPhrases) + len(symptomsFound) > 0):

                    polarity = sentenceScore / abs(sentenceScore)
                    symptomState = naturalLanguageWhiz.symptomNegWordStructureCheck(sentence, polarity, symptomsFound, argExtractor)
                    logging.info('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                    if(symptomState is True):
                        logging.info('HACK: Symptom Persists/ Worsening : Presence of negative verb + Symptoms')
                    else:
                        logging.info('HACK: Possibly Worsened Symptom: Presence of Symptom but no verb found')    
                    logging.info(symptomsFound)
                    logging.info(sentence)


            post.setPositiveWordScore(str(postWordScore))
            emotion = argExtractor.checkForEmotion(post)
            post.setEmotion(emotion)

        logging.info('Completed [main]: Finished searching for symptoms and diseases within the posts')

    # Now run through and print off the list of symptoms and diseases found relative to the drug
    # In this simple script we have taken the reviews on tamoxifen 
    displayArguments.constructXML(forums)
    logging.info('End of [main]: Processed: ' + str(postCount) + ' posts')
    logging.info('Finished [main]: Finished Process Succesfully')


if __name__ == "__main__": main()