import postsGatherer
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from nltk.corpus import movie_reviews

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

forums = postsGatherer.gatherForums()

trainingSet = []

posts = forums[0].getPosts()

i = 0
for post in posts:
    
    sentiment = 'neg'
    if(post.getRating() <= 5):
        sentiment = 'neg'
    else:
        sentiment = 'pos'

    trainingSet.append((post.getReview(), sentiment))
    i = i + 1


cl = NaiveBayesClassifier(trainingSet)

print(cl.classify(posts[0].getReview()))
print(cl.show_informative_features(5))
print('finished')