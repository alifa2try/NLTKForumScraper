from ModelLayer.argumentExtractor import argumentExtractor
from ModelLayer import naturalLanguageWhiz
import logging 

logger = logging.getLogger(__name__)

''' This class contains all of the rules for detecting sentiment related content

'''

class experienceExtractor(object):

    def __init__(self):
        self.sentence = ''
        self.experience = ''
        self.treatment = ''

    def checkForMentionOfSentimentOnly(self, sentence, sentenceScore, symptomsFound, drugsFound, treatment, argExtractor, dbobj):

        if (sentenceScore != 0) and (len(symptomsFound) == 0) and (len(drugsFound) == 0):
            polarity = sentenceScore / abs(sentenceScore)

            if polarity > 0:
                experience = 'Positive Experience - No symptoms mentioned but positive words found'
            if polarity < 0:
                experience = 'Negative Experience - No symptoms mentioned but negative words found'  
            

            self.experience = experience
            self.sentence = sentence
            self.treatment = treatment
            #insertIntoDB(sentence, experience, treatment, dbobj)          


    def insertIntoDB(sentence, experience, treatment, dbobj):

        sqlSentence = (sentence.replace("'","\\'"))

        insertSql = "INSERT INTO Experiences (Sentence, Experience, Drug) VALUES (%s, %s, %s);" % ("'"+ sqlSentence + "'", "'"+ experience + "'", "'" + treatment + "'")

        dbobj.insert(insertSql)

    def insertIntoDB(self, post, dbobj):

        sqlSentence = (self.sentence.replace("'","\\'"))

        insertSql = "INSERT INTO Experiences (Post, Sentence, Experience, Drug) VALUES (%s ,%s, %s, %s);"
        data = (post, sqlSentence, self.experience, self.treatment)
        dbobj.insert(insertSql, data)