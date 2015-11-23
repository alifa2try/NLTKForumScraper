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
        self.symptoms = []
        self.disease = []
        self.experience = []
        self.sentiment = []

    def getReview(self):
        return self.review

    def getRating(self):
        return self.rating

    def getSymptoms(self):
        return self.symptoms

    def getDisease(self):
        return self.disease

    def getExperience(self):
        return self.experience

    def getUrl(self):
        return self.url
    
    def getSentiment(self):
        return self.sentiment
    
    def setSymptoms(self,symptom):
        self.symptoms.append(symptom)

    def setDisease(self, disease):
        self.disease.append(disease)

    def setExperience(self, experience):
        self.experience.append(experience)

    def setSentiment(self, sentiment):
        self.sentiment = sentiment



