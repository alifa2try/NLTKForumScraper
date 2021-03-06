class post(object):
    """A post is a single online review

       Attributes:
            Review: This is the content of the review
            Rating: This is the rating the user gave to the product
    """

    def __init__(self, review, rating, url):
        self.review = review
        self.rating = rating
        self.url = url
        # The following properties are to be set by argument extractor
        self.reliefs = []
        self.symptoms = []
        self.disease = []
        self.drugs = []
        self.emotion = ''
        self.sentiment = []
        self.symptomDrugRelation = []
        self.positiveWordScore = ''
        self.nounPhrases = []

    # All the GETS go here
    
    def getReview(self):
        return self.review

    def getRating(self):
        return self.rating

    def getSymptoms(self):
        return self.symptoms
    
    def getReliefs(self):
        return self.reliefs

    def getDisease(self):
        return self.disease

    def getDrugs(self):
        return self.drugs

    def getEmotion(self):
        return self.emotion

    def getUrl(self):
        return self.url
    
    def getSentiment(self):
        return self.sentiment

    def getSymptomDrugRelation(self):
        return self.symptomDrugRelation

    def getPositiveWordScore(self):
        return self.positiveWordScore
    
    def getNounPhrases(self):
        return self.nounPhrases

    # All the SETS go here
    def setReview(self, review):
        self.review = review

    def setSymptoms(self,symptom):
        self.symptoms.append(symptom)

    def setReliefs(self,relief):
        self.reliefs.append(relief)

    def setDisease(self, disease):
        self.disease.append(disease)

    def setDrugs(self, drug):
        self.drugs.append(drug)

    def setEmotion(self, emotion):
        self.emotion = emotion

    def setSentiment(self, sentiment):
        self.sentiment = sentiment

    def setSymptomDrugRelation(self, symptomDrugRelation):
        self.symptomDrugRelation.append(symptomDrugRelation)

    def setPositiveWordScore(self, positiveWordScore):
        self.positiveWordScore = positiveWordScore

    def setNounPhrase(self, nounPhrase):
        self.nounPhrases.append(nounPhrase)


