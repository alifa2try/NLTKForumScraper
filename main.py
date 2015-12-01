import nltk  
import medicalInfoGatherer
import postsGatherer
import forum
import logging
import displayArguments
import argumentExtractor

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

            postWordScore = 0

            for sentence in sentences:
                    
                postWordScore = postWordScore + argumentExtractor.calculateWordScore(sentence)

                foundSymptom , symptom = argumentExtractor.checkForSymptomInClause(sentence, listOfSymptoms)
                # Make sure that we do not append a symptom twice.It may be the case that the post mentions a symptom twice in two or more sentences
                if(foundSymptom and symptom not in post.getSymptoms()):
                    post.setSymptoms(symptom)

                foundDisease , disease = argumentExtractor.checkForDiseaseInClause(sentence, listOfDiseases)
                if(foundDisease and disease not in post.getDisease()):
                    post.setDisease(disease)

            post.setPositiveWordScore(str(postWordScore))
            emotion = argumentExtractor.checkForEmotion(post)
            post.setEmotion(emotion)

        logging.info('Completed [argumentExtractor]: Finished searching for symptoms and diseases within the posts')

    # Now run through and print off the list of symptoms and diseases found relative to the drug
    # In this simple script we have taken the reviews on tamoxifen 
    displayArguments.constructXML(forums)
    logging.info('Finished [argumentExtractor]: Finished Process Succesfully')


if __name__ == "__main__": main()