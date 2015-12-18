"""This module will gather the posts from the various forums
"""
from bs4 import BeautifulSoup
import requests
import re
from DataLayer.post import post
from DataLayer.forum import forum
from Utilities import messageCleaner
import logging
from DataLayer.dataBaseConnector import dataBaseConnector
import pymysql.cursors

logger = logging.getLogger(__name__)

# This is the main function to be called from within this module
def gatherForums():
    
    forums = __instantiateForumsLists()

    __insertIntoDB(forums)

    return forums

# This is a class used to gather all of the various forum posts 
def __instantiateForumsLists():

    forums = []

    # Here append all of the forums
    # Drugs.com - all of the urls are to be appended to this list:
    drugsdotcom = []
    drugsdotcom.append('http://www.drugs.com/comments/tamoxifen/for-breast-cancer.html')
    drugsdotcom.append('http://www.drugs.com/comments/naproxen/')
      
    for forum in drugsdotcom:
        forums.append(__gatherDrugsCom(forum))

    webmd = []
    # WebMD.com - all of the urls to the appended to this list
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=0&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=1&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=2&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=3&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=4&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=5&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=6&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=7&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=8&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=9&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=10&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=11&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=12&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=13&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=14&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=15&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=16&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=17&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=18&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=19&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=20&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=21&sortby=3&conditionFilter=-500')
    webmd.append('http://www.webmd.com/drugs/drugreview-4497-tamoxifen+oral.aspx?drugid=4497&drugname=tamoxifen+oral&pageIndex=22&sortby=3&conditionFilter=-500')
    
    for forum in webmd:
        forums.append(__gatherWebMD(forum))

    return forums

# Use this section to define all of the forum scrapers to be used
def __gatherDrugsCom(url):

    forumName = 'Drugs.com'
    results = requests.get(url)
    soup = BeautifulSoup(results.content, 'html.parser')

    rawPosts = soup.find_all(name = "div",  attrs = {'class' : 'boxList'})
    posts = []
    maxRating = 10

    # Extract the reviews and the ratings. If a post does not provide a review and a rating we will
    # dismiss it because it will not be useful during the learning phase
    
    for rawPost in rawPosts:

        try:
            review = rawPost.find(name = "div",  attrs = {'class' : 'user-comment'})
            review = review.find(name = "span").get_text()

            rating = rawPost.find(name = "div",  attrs = {'class' : 'rating-score'}).get_text()

        except:
            logger.error(" Error[__gatherDrugsCom(url)] = Threw an error whilst looking for a review or rating")
            continue

        # Removing special characters here
        review = messageCleaner.removeSpecialCharacter(review)

        if(review and rating):
            forumPost = post(review, __scaleRatings(rating, maxRating), url)
            posts.append(forumPost)
    
    drugsComForum = forum(forumName , url, maxRating, posts)
    return drugsComForum

def __gatherWebMD(url):
    # WebMD is problamtic in that it provides three types of ratings. To simplify the problem we will only be pulling the satisfaction rating, as this 
    # seems to be the most general one 
    forumName = 'Webmd.com'
    results = requests.get(url)
    soup = BeautifulSoup(results.content, 'html.parser')

    rawPosts = soup.find_all(name="div", attrs = {'class' : 'userPost'})
    posts = []
    maxRating = 5

    for rawPost in rawPosts:

        try: 
            review = rawPost.find(name = "p" , attrs = {'id' : re.compile('comFull.*')}).get_text()
            rating = rawPost.find(name = "div" , attrs = {'class' : 'catRatings lastEl clearfix'}).get_text()

        except:
            print(" Error[__gatherWebMD(url)]= Threw an error whilst looking for a review or rating")
            continue

        # Removing special characters here
        review = messageCleaner.removeSpecialCharacter(review)
        rating = re.findall('\d+', rating)
        if(review and rating):
            forumPost = post(review, __scaleRatings(rating[0], maxRating), url)
            posts.append(forumPost)

    webMD = forum(forumName, url, maxRating, posts)
    return webMD

def __scaleRatings(rating, maxValue):
    # We will scale all of the ratings to ten
    rating = float(rating)
    scaledRating = (rating / maxValue) * 10
    return str(scaledRating)

def __insertIntoDB(forums):

    dbobj = dataBaseConnector('DBConnector.ini')

    for forum in forums:
        for post in forum.getPosts():
            message = post.getReview()
            message = message.replace("'","\\'")

            url = forum.getURL()
            url = url.replace("'","\\'")
            forumName = forum.getName()


            insertSql = "INSERT INTO ForumPosts (ForumName, URL, Post) VALUES (%s, %s, %s);" % ("'"+ forumName + "'", "'"+ url + "'", "'"+ message + "'")
            dbobj.insert(insertSql)








    

