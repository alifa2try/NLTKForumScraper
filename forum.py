class forum(object):
    """This class is used to encapsulate a single forum. 
    
    In it we will have a list of posts, and a rating
    
    Attributes:
        url: This will hold the url of the class
        posts: This will hold a set of posts object
    """

    def __init__(self, url, posts):
        self.url = url
        self.posts = posts

    def getPosts(self):
        return self.posts

    def getURL(self):
        return self.url 





