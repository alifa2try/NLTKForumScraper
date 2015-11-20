import messageCleaner
import postsGatherer
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from nltk.corpus import movie_reviews


forums = postsGatherer.gatherForums()

trainingSet = []
posts = []

i = 0
for post in forums[0].getPosts():
    if(post.getRating() <= 7):
        sentiment = 'neg'
    else:
        sentiment = 'pos'

    trainingSet.append((messageCleaner.removeStopWords(post.getReview()), sentiment))
    i = i + 1

testSet = []
for post in forums[1].getPosts():
    if(post.getRating() <= 7):
        sentiment = 'neg'
    else:
        sentiment = 'pos'

    testSet.append((messageCleaner.removeStopWords(post.getReview()), sentiment))
    i = i + 1


cl = NaiveBayesClassifier(trainingSet)

print('REVIEW\t\t\tACTUAL\n')

for post in forums[1].getPosts():
    print(cl.classify(post.getReview()),'\t\t\t', post.getRating())

print('finished')

    




print(cl.classify(posts[0].getReview()))
print(cl.show_informative_features(5))
print('finished')