from ModelLayer.argumentExtractor import argumentExtractor
from ModelLayer import naturalLanguageWhiz
import logging 

logger = logging.getLogger(__name__)

''' This class contains all of the rules for detecting the severity of symptoms

'''
class symptomConditionExtractor(object):

    def __init__(self):
        self.sentence = ''
        self.symptomCriticality = ''
        self.symptomFound = ''
        self.treatment = ''

    def checkSymptomConditions(self, sentence, sentenceScore,  symptomsFound, treatment, argExtractor, dbobj):

        if (sentenceScore != 0) and (len(symptomsFound) > 0):

            polarity = sentenceScore / abs(sentenceScore)
            symptomState = naturalLanguageWhiz.symptomNegWordStructureCheck(sentence, polarity, symptomsFound, argExtractor)

            if(symptomState and polarity < 0):
                self.symptomCriticality = 'Symptoms are bad: Presence of negative verb + symptoms'
            elif(symptomState and polarity > 0):
                self.symptomCriticality = 'Symptoms are ok: Presence of positive verb + symptoms'
            else:
                self.symptomCriticality = 'Symptoms are possibly bad: symptoms mentioned but no verb found'
            
            self.sentence = sentence
            self.symptomFound = symptomsFound[0]
            self.treatment = treatment
            #insertIntoDB(sentence, symptomCriticality, symptomsFound[0], treatment, dbobj)   



    def insertIntoDB(sentence, symptomCriticality, symptomFound, treatment, dbobj):

        sqlSentence = (sentence.replace("'","\\'"))

        insertSql = "INSERT INTO SymptomCondition (Sentence, SymptomCriticality, Symptom, Drug) VALUES (%s, %s, %s, %s);" % ("'"+ sqlSentence + "'", "'"+ symptomCriticality + "'", "'"+ symptomFound + "'", "'" + treatment + "'")

        dbobj.insert(insertSql)

    def insertIntoDB(self, post, dbobj):

        sqlSentence = (self.sentence.replace("'","\\'"))

        insertSql = "INSERT INTO SymptomCondition (Post, Sentence, SymptomCriticality, Symptom, Drug) VALUES (%s, %s, %s, %s, %s);" 
        data = (post, sqlSentence, self.symptomCriticality, self.symptomFound, self.treatment)
        dbobj.insert(insertSql, data)