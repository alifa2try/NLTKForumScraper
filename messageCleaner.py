from nltk.corpus import stopwords
import re

# Function to remove escape characters and the like
def removeSpecialCharacter(message):
    messageCleaned = message.strip()
    # " ".join(message.split())
    # TODO: Make sure to recomment this again. This was changed so we can only remove white spaces for the diseaseGatherer module
    #messageCleaned = re.sub("[^a-zA-Z]", " ", message)
    return messageCleaned

# Function to remove stopwords from each of the messages
def removeStopWords(message):

    stopWords = set(stopwords.words("english"))  
    
    # Seperate the element out into inidvidual words
    messageWords = re.compile('\w+').findall(message)

    meaningfulWords = []
    # Strip the message of Stopwords and place them into the meaningfulWords container
    for word in messageWords:
        if word not in stopWords:
            meaningfulWords.append(word)

    return(" ".join(meaningfulWords))

