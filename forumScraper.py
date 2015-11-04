from bs4 import BeautifulSoup
import csv
import requests

# Insert the forum link here. Gather the HTML from the forum into a requests oject. Insert
forumURL = "https://forum.breastcancercare.org.uk/t5/Chemotherapy/Not-sure-if-to-have-chemo-or-not/td-p/723779"
results = requests.get(forumURL)

# Convert the forum page into a BeautifulSoup object
soup = BeautifulSoup(results.content, 'html.parser')

posts = soup.findAll('ul', class_= "lia-message-body-content")

print(len(posts))
