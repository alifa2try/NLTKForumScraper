class post(object):
    """A post is a single online review

       Attributes:
            Review: This is the content of the review
            Rating: This is the rating the user gave to the product
    """

    def __init__(self, review, rating):
        self.review = review
        self.rating = rating

    def getReview(self):
        return self.review

    def getRating(self):
        return self.rating


