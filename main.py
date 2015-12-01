import nltk  
import medicalInfoGatherer
import postsGatherer
import forum
import logging
import displayArguments
from argumentExtractor import argumentExtractor
import messageCleaner

def main():
    logging.basicConfig(filename='log.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    # Gather the posts from all of the forums and the list of necessary medical terms 

    logging.info('-------------------------------------------------------')
    logging.info('-------------Starting Argument Extractor---------------')
    logging.info('-------------------------------------------------------')

    logging.info('Starting [main]: Building data lists')
    forums = postsGatherer.gatherForums()
    listOfDiseases = medicalInfoGatherer.getListofDiseases()
    listOfSymptoms = medicalInfoGatherer.getListofSymptoms()

    posWords = 'Data/positive-words.txt'
    negWords = 'Data/negative-words.txt'
    invWords = 'Data/inverter-words.txt'

    with open(posWords, encoding = 'utf-8') as f:
        posData = f.readlines()
  
    posList = []
    for member in posData: 
        member = messageCleaner.removeSpecialCharacter(member)
        posList.append(member)

    with open(negWords, encoding = 'utf-8') as f:
        negData = f.readlines()
  
    negList = []
    for member in negData: 
        member = messageCleaner.removeSpecialCharacter(member)
        negList.append(member)

    with open(invWords, encoding = 'utf-8') as f:
        invData = f.readlines()
  
    invList = []
    for member in invData: 
        member = messageCleaner.removeSpecialCharacter(member)
        invList.append(member)


    
    logging.info('Finished [main]: Finished building data lists')
    
    argExtractor = argumentExtractor(listOfSymptoms, listOfDiseases, invList, posList, negList)
    # Loop through each of the forum posts and print the arguments onto the page. The arguments for and against each of the posts.
    # Some sort of extremley Naive Bayesian classifier 

    for forum in forums:
        posts = forum.getPosts()

        logging.info('Starting [main]: Beginning to search for symptoms and diseases within the posts')

        for post in posts:
            sentences = nltk.sent_tokenize(post.getReview())

            postWordScore = 0

            for sentence in sentences:

                postWordScore = postWordScore + argExtractor.calculateWordScore(sentence)

                foundSymptom , symptom = argExtractor.checkForSymptomInClause(sentence)
                # Make sure that we do not append a symptom twice.It may be the case that the post mentions a symptom twice in two or more sentences
                if(foundSymptom and symptom not in post.getSymptoms()):
                    post.setSymptoms(symptom)

                foundDisease , disease = argExtractor.checkForDiseaseInClause(sentence)
                if(foundDisease and disease not in post.getDisease()):
                    post.setDisease(disease)

            post.setPositiveWordScore(str(postWordScore))
            emotion = argExtractor.checkForEmotion(post)
            post.setEmotion(emotion)

        logging.info('Completed [main]: Finished searching for symptoms and diseases within the posts')

    # Now run through and print off the list of symptoms and diseases found relative to the drug
    # In this simple script we have taken the reviews on tamoxifen 
    displayArguments.constructXML(forums)
    logging.info('Finished [main]: Finished Process Succesfully')


if __name__ == "__main__": main()