import nltk  
import medicalInfoGatherer
import postsGatherer
import forum
import logging
import displayArguments

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

"""The argument extraction script begins here:

    1. First we pull in list of forum posts
    2. We then pull in list of medical diseases and symptoms
    3. For each of the posts we search for the presence of symptoms or diseases in the tokenised posts
"""

def main():
    logging.basicConfig(filename='log.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    # Gather the posts from all of the forums and the list of necessary medical terms 

    logging.info('-------------------------------------------------------')
    logging.info('-------------Starting Argument Extractor---------------')
    logging.info('-------------------------------------------------------')

    forums = postsGatherer.gatherForums()
    listOfDiseases = medicalInfoGatherer.getListofDiseases()
    listOfSymptoms = medicalInfoGatherer.getListofSymptoms()

    symptomsFound = []
    diseasesFound = []

    # Loop through each of the forum posts and print the arguments onto the page. The arguments for and against each of the posts.
    # Some sort of extremley Naive Bayesian classifier 

    for forum in forums:
        posts = forum.getPosts()

        logging.info('Starting [argumentExtractor]: Beginning to search for symptoms and diseases within the posts')

        for post in posts:
            sentences = nltk.sent_tokenize(post.getReview())

            for sentence in sentences:
                foundSymptom , symptom = checkForSymptomInClause(sentence, listOfSymptoms)
                # Make sure that we do not append a symptom twice.It may be the case that the post mentions a symptom twice in two or more sentences
                if(foundSymptom and symptom not in post.getSymptoms()):
                    symptomsFound.append(symptom)
                    post.setSymptoms(symptom)

                foundDisease , disease = checkForDiseaseInClause(sentence, listOfDiseases)
                if(foundDisease and disease not in post.getDisease()):
                    diseasesFound.append(disease)
                    post.setDisease(disease)

            emotion = checkForEmotion(post)
            post.setEmotion(emotion)

        logging.info('Completed [argumentExtractor]: Finished searching for symptoms and diseases within the posts')

    # Now run through and print off the list of symptoms and diseases found relative to the drug
    # In this simple script we have taken the reviews on tamoxifen 
    displayArguments.constructXML(forums)
    logging.info('Finished [argumentExtractor]: Finished Process Succesfully')


if __name__ == "__main__": main()