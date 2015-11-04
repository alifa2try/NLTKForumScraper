from bs4 import BeautifulSoup
import csv
import requests

# Insert the forum link here. Gather the HTML from the forum into a requests oject. Insert
results = requests.get('https://forum.breastcancercare.org.uk/t5/Chemotherapy/Not-sure-if-to-have-chemo-or-not/td-p/723779')
forumContent = results.content

# Convert the forum page into a BeautifulSoup object
soup = BeautifulSoup(forumContent, 'html.parser')

print(soup.prettify())



