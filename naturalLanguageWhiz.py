import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from argumentExtractor import argumentExtractor

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

def tag(sentence):

    try:
        tokenizer = PunktSentenceTokenizer(sentence)
        tokenized = tokenizer.tokenize(sentence)

        words = nltk.word_tokenize(tokenized[0])
        tagged = nltk.pos_tag(words)

        print(tagged)

        return tagged

    except Exception as e:
        print(str(e))


def symptomNegWordStructureCheck(sentence, polarity, symptoms, argExtractor):

    sentimentWords = argExtractor.extractSentimentWords(sentence, polarity)
    taggedSentence = tag(sentence)
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




