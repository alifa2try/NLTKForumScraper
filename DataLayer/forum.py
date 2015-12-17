class forum(object):
    """This class is used to encapsulate a single forum. 
    
    In it we will have a list of posts, and a rating
    
    Attributes:
        url: This will hold the url of the class
        posts: This will hold a set of posts object
    """

    def __init__(self, forumName, url, maxScore, posts):
        self.forumName = forumName
        self.url = url
        self.maxScore = maxScore
        self.posts = posts

    def getName(self):
        return self.forumName

    def getPosts(self):
        return self.posts

    def getURL(self):
        return self.url 

    def getAverageReview(self):

        sum = 0
        for post in self.posts:
            sum += post.rating

        average = sum / len(self.posts)
        return average

    def getmaxScore(self):
        return maxScore




