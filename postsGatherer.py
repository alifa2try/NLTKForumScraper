"""This module will gather the posts from the various forums
"""
from bs4 import BeautifulSoup
import requests
from post import post
from forum import forum
import messageCleaner

# This is the main class to be called from within the module
def gatherPosts():
    
    forums = __instantiateForumsLists()

    return forums

# This is a class used to gather all of the various forum posts 
def __instantiateForumsLists():

    forums = []

    # Here append all of the forums
    forums.append(__gatherDrugsCom())

    return forums

# Use this section to define all of the forum scrapers to be used
def __gatherDrugsCom():

    url = 'http://www.drugs.com/comments/tamoxifen/for-breast-cancer.html'
    results = requests.get(url)
    soup = BeautifulSoup(results.content, 'html.parser')

    rawPosts = soup.find_all(name = "div",  attrs = {'class' : 'boxList'})
    soup.f
    posts = []

    # Extract the reviews and the ratings. If a post does not provide a review and a rating we will
    # dismiss it because it will not be useful during the learning phase
    

    for rawPost in rawPosts:

        try:
            review = rawPost.find(name = "div",  attrs = {'class' : 'user-comment'}).get_text()
            rating = rawPost.find(name = "div",  attrs = {'class' : 'rating-score'}).get_text()

        except:
            print("A key value not provided")
            continue

        messageCleaner.removeSpecialCharacter(review)

        if(review and rating):
            forumPost = post(review, rating)
            posts.append(forumPost)


    drugsComForum = forum(url, posts)
    return drugsComForum

gatherPosts()