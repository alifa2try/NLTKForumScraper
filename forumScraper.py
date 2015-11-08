from bs4 import BeautifulSoup
import messageCleaner
import bagOfWords
import csv
import requests

# Insert the forum links here. Gather the HTML from the forum into a requests oject. Insert
# TODO : Place these into a set for easier access
forumURL = "https://forum.breastcancercare.org.uk/t5/Chemotherapy/Not-sure-if-to-have-chemo-or-not/td-p/723779"
forumURL2 = "https://forum.breastcancercare.org.uk/t5/Chemotherapy/Not-sure-if-to-have-chemo-or-not/td-p/723779/page/2"


def extractMessages(forumURL):
    results = requests.get(forumURL)
    

    # Convert the forum page into a BeautifulSoup object
    soup = BeautifulSoup(results.content, 'html.parser')

    # Pull out the correct tag from the HTML
    posts = soup.find_all(name ='div', attrs = {'class' : 'lia-message-body-content'})

    # Have only the message content and remove any HTML tags
    postsMessages = []
    for post in posts:
        postsMessages.append(post.get_text())

    print(len(postsMessages))
    
    return postsMessages

# Grab forum posts from both pages.
# TODO: Think of better way to do this. Maybe use a list?
postsForum = extractMessages(forumURL)
postsForum2 = extractMessages(forumURL2)

for post in postsForum2:    
    postsForum.append(post)

print('Total length: \n')
print(len(postsForum))

# Clean all of the messages by removing 
for post in postsForum:
    post = messageCleaner.removeSpecialCharacter(post)
    post = messageCleaner.removeStopWords(post)


# Now pass the message list through a either a BoW model first
#postsMessagesFeatures = bagOfWords.vectorizeMessage(postsMessages)

    





