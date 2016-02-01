from nltk.tokenize import word_tokenize
from DataLayer import medicalInfoGatherer
from DataLayer import postsGatherer
from DataLayer import forum
import logging
from ViewLayer import displayArguments
from Utilities import messageCleaner

class argumentExtractor(object):


    def __init__(self, listOfSymptoms, listOfDiseases, listOfDrugs, listOfInverters, listOfPosWords, listOfNegWords, listOfContractions):
        self.listOfSymptoms = listOfSymptoms
        self.listOfDiseases = listOfDiseases
        self.listOfDrugs = listOfDrugs
        self.listOfInverters = listOfInverters
        self.listOfPosWords = listOfPosWords
        self.listOfNegWords = listOfNegWords
        self.listOfContractions = listOfContractions


    def getListOfSymptoms(self):
        return self.listOfSymptoms

    def getListOfDiseases(self):
        return self.listOfDiseases

    def getListOfDrugs(self):
        return self.listOfDrugs

    def getListOfInverters(self):
        return self.listOfInverters

    def getListOfPosWords(self):
        return self.listOfPoswords

    def getListOfContractions(self):
        return self.listOfContractions


    def checkForDrugs(self, sentence):
        drugs = []

        for drug in self.listOfDrugs:
            if drug.lower() in sentence.lower():
                drugs.append(drug.lower())
         
        return drugs

    def checkForSymptomInClause(self, sentence):
        
        sentenceTokenised = word_tokenize(sentence)
        symptoms = []
        relief = []

        for symptom in self.listOfSymptoms:
            if symptom.lower() in sentence.lower():
                symptoms.append(symptom.lower())
        
        return symptoms, relief

    def checkdrugSymptomRelation(self, symptomsFound, drugsFound, sentence):

        symDrugRelation = []

        if(len(symptomsFound) > 0 and len(drugsFound) > 0):
            for symptom in symptomsFound:
                # TODO: This is a naive assumption that we'll only have a few drugs mentioned. Needs to be changed
                symDrugRelation.append([symptom, drugsFound[0]])

        return symDrugRelation

    def checkForDiseaseInClause(self, sentence):

        for disease in self.listOfDiseases:
            if disease.lower() in sentence.lower():
                return (True, disease)

        return (False,'')

    def checkForEmotion(self, post):
        ratingCategory = ''
        volumeofDisSymptms = ''
        emotion = ''

        # Get the rating level
        rating = float(post.getRating())
        if rating <= 3:
            ratingCategory = 'low'
        elif rating >= 7:
            ratingCategory = 'high'
        else:
            ratingCategory = 'med'

        # Gauge the volume of symptoms and symptoms
        noOfSymptoms = len(post.getSymptoms())
        noOfDiseases = len(post.getDisease())
  
        if (noOfDiseases + noOfSymptoms) < 1:
            volumeofDisSymptms = 'low'
        elif (noOfDiseases + noOfSymptoms) == 1:
            volumeofDisSymptms = 'med'
        else:
            volumeofDisSymptms = 'high'

        # Primitive rules for getting the emotion
        if (volumeofDisSymptms is 'high' and ratingCategory is 'low'):
            emotion = 'unoptimisitic'
        elif (volumeofDisSymptms is 'high' and ratingCategory is 'high'):
            emotion = 'optimistic'
        elif (volumeofDisSymptms is 'low' and ratingCategory is 'high'):
            emotion = 'positive'
        else:
            emotion = 'neutral'

        return emotion

    def calculateWordScore(self, sentence):
        # import neg and pos words
        # count the number of pos words in the sentence
        # count the number of neg words in the sentence
        # do a sum of the two: score = posCount - negCount
        sentenceTokenised = word_tokenize(sentence)
        if sentenceTokenised is None:
            return 0

        negScore = 0
        posScore = 0

        for i, word in enumerate(sentenceTokenised):
            score = self.getInverterScore(word, i, sentenceTokenised, self.listOfPosWords)
            score = score + (self.getInverterScore(word, i, sentenceTokenised, self.listOfNegWords) * -1)
            if score < 0:
                negScore = negScore + score
            else:
                posScore = posScore + score

        totalScore = posScore + negScore

        return totalScore

    def getInverterScore(self, word, index, sentence, list):

        """This method will search for inverters like 'not', 'no' etc. 
            It works as follows:
                1. Search to see if the word exists in the list you are searching in
                    1. If it is the first word in the sentence (known from its index) assume it as a positive existance and return 1
                    2. If it is not the first word in the sentence, it may be that there is an inverter before it
                        1. If there is an inverter assume that it is a negative existance and return -1
                        2. Id there is not an inveter assum that it is a positive existance and return 1
                    3. If the word does not exist at all return 0
        """
        lowerCaseList = [element.lower() for element in list]

        if word.lower() in lowerCaseList:
            if index > 0:
                if sentence[index - 1].lower() in self.listOfInverters:
                    return -1
                else:
                    return 1
            else:
                return 1
        else:
            return 0
    
    def checkIfInverterWordEndOfSentence(self, sentence):

        ''' This method checks to see if the last word in the sentence is an inverter word. This is useful if you want to 
            see if you have an inverter word before a keyword. In order to use this function you need to strip the sentence
            preceeding your keyword and then pass the stipped sentence into here. The sentence needs to then be POS tagged, so 
            we can interate over the words
        '''
        # TODO: Note that we will not catch noun phrases like lack of in the preceeding sentences

        lowerCaseList = [element.lower() for element in self.listOfInverters]
        lastWordInSentence = sentence[-1]

        for word in lowerCaseList:
            if lastWordInSentence[0] == word:
                return True
        
        return False


    def checkIfInverterWordInSentence(self, sentence):

        lowerCaseList = [element.lower() for element in self.listOfInverters]

        for word in sentence:
            for inverter in lowerCaseList:
                if inverter == word[0]:
                    return True
        
        return False



    def extractSentimentWords(self, sentence, polarity):
        
        sentimentWords = []
        words = word_tokenize(sentence)

        posList = [element.lower() for element in self.listOfPosWords]
        negList = [element.lower() for element in self.listOfNegWords]


        if polarity > 0:
            for word in words:
                if word.lower() in posList:
                    sentimentWords.append(word)
        else:
            for word in words:
                if word.lower() in negList:
                    sentimentWords.append(word)

        return sentimentWords

    
            

