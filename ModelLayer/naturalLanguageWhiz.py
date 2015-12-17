import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from ModelLayer.argumentExtractor import argumentExtractor 

def extractNounPhrases(sentence):

    nounPhrases = []
    try:
        tokenizer = PunktSentenceTokenizer(sentence)
        tokenized = tokenizer.tokenize(sentence)

        words = nltk.word_tokenize(tokenized[0])
        tagged = nltk.pos_tag(words)

        firstNN = False
        

        for tag in tagged:
            pos = tag[1]
            if 'NN' in pos:
                if firstNN:
                    nounPhrase = firstNoun + ' ' + tag[0]
                    nounPhrases.append(nounPhrase)
                    firstNN = False
                    continue
                else:
                    firstNoun = tag[0]
                    firstNN = True
                    continue

            firstNN = False
            

    except Exception as e:
         print(str(e))

    return nounPhrases

def __tag(sentence):

    try:
        tokenizer = PunktSentenceTokenizer(sentence)
        tokenized = tokenizer.tokenize(sentence)

        words = nltk.word_tokenize(tokenized[0])
        tagged = nltk.pos_tag(words)

        return tagged

    except Exception as e:
        print(str(e))


def symptomNegWordStructureCheck(sentence, polarity, symptoms, argExtractor):

    sentimentWords = argExtractor.extractSentimentWords(sentence, polarity)
    taggedSentence = __tag(sentence)
    sentiWordisVerbType = False

    for sentimentWord in sentimentWords:
        for postag in taggedSentence:
            if sentimentWord.lower() in postag[0].lower():
                if 'VB' in postag[1]:
                    sentiWordisVerbType = True
                    break
                index = taggedSentence.index(postag)
                if index > 0:
                    precdTag = taggedSentence[index - 1]
                    if 'VB' in precdTag:
                        sentiWordisVerbType = True
                        break
    
    return sentiWordisVerbType

def extractConnectingVerbs(sentence, symptoms, drugs, dbobj):

    if len(symptoms) <= 0 or len(drugs) <= 0:
        return

    taggedSentence = __tag(sentence)
    symptomPos = 0
    symptom = ''
    drug = ''
    drugPos = 0
    connectingVerbs = []
    drugFirst = 'Y'

    for idx, posTag in enumerate(taggedSentence):
        if posTag[0].lower() in symptoms:
            symptomPos = idx
            symptom = posTag[0]
            continue
        if posTag[0].lower() in drugs:
            drugPos = idx
            drug = posTag[0]
            continue
        if ((symptom != '') or (drug != '')):
            if 'VB' in posTag[1]:
                connectingVerbs.append(posTag[0])
                continue
        if ((symptom != '') and (drug != '') and (len(connectingVerbs) > 0)):
            
            if drugPos < symptomPos:
                drugFirst = 'Y'
            else:
                drugFirst = 'N'

            for verb in connectingVerbs:

                sentence = (sentence.replace("'","\\'"))

                insertSql = "INSERT INTO SentenceDetails (Sentence, ConnectingVerb, Symptoms, Drugs, DrugsFirst) VALUES (%s, %s, %s, %s, %s);" % ("'"+ sentence + "'", "'"+ verb + "'", "'"+ symptom + "'", "'"+ drug + "'", "'"+ drugFirst + "'")
                dbobj.insert(insertSql)

            break
    

    







