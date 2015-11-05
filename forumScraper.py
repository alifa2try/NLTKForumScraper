from bs4 import BeautifulSoup
import csv
import requests

# Insert the forum link here. Gather the HTML from the forum into a requests oject. Insert
forumURL = "https://forum.breastcancercare.org.uk/t5/Chemotherapy/Not-sure-if-to-have-chemo-or-not/td-p/723779"
results = requests.get(forumURL)

# Convert the forum page into a BeautifulSoup object
soup = BeautifulSoup(results.content, 'html.parser')

# Pull out the correct tag from the HTML
posts = soup.find_all(name ='div', attrs = {'class' : 'lia-message-body-content'})

# Have only the message content and remove any HTML tags
postsMessages = []
for post in posts:
    postsMessages.append(post.get_text())

# Pass it through a BagofWords model
for message in postsMessages:
    print(message)





