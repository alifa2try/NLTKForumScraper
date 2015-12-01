from nltk.tokenize import word_tokenize
import medicalInfoGatherer
import postsGatherer
import forum
import logging
import displayArguments
import messageCleaner

def checkForSymptomInClause(sentence, listOfSymptoms):
    
    for symptom in listOfSymptoms:
        if symptom.lower() in sentence.lower():
            return (True, symptom)
        
    return (False, '')

def checkForDiseaseInClause(sentence, listOfDiseases):

    for disease in listOfDiseases:
        if disease.lower() in sentence.lower():
            return (True, disease)

    return (False,'')

def checkForEmotion(post):
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

def calculateWordScore(sentence):
    # import neg and pos words
    # count the number of pos words in the sentence
    # count the number of neg words in the sentence
    # do a sum of the two: score = posCount - negCount
    sentenceTokenised = word_tokenize(sentence)

    posWords = 'Data/positive-words.txt'
    negWords = 'Data/negative-words.txt'

    with open(posWords) as f:
        posData = f.readlines()
  
    posList = []
    for member in posData: 
        member = messageCleaner.removeSpecialCharacter(member)
        posList.append(member)

    with open(negWords) as f:
        negData = f.readlines()
  
    negList = []
    for member in negData: 
        member = messageCleaner.removeSpecialCharacter(member)
        negList.append(member)
    

    sentenceTokenisedSet = set(sentenceTokenised)
    posListSet = set(posList)
    negListSet = set(negList)

    posMatches = sentenceTokenisedSet.intersection(posListSet)
    negMatches = sentenceTokenisedSet.intersection(negListSet)

    score = len(posMatches) - len(negMatches)

    return score
