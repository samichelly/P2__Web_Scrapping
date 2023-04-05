import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import pandas
from PIL import Image


"""
#def parser_one_book(URL):

#Récupérer le contenu de la page HTML + création objet Soup OK
URL = 'http://books.toscrape.com/catalogue/chase-me-paris-nights-2_977/index.html'
nb_URL = 1
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'lxml')

#Extraction titre OK
titre = soup.find(class_="col-sm-6 product_main").h1.text

#Extraction description OK
descript = soup.find(class_="product_page").findChildren('p')
description = descript[3].text
print(description)

#Extraction catégorie OK
soup_categorie = soup.find_all('class_="breadcrumb"' and 'li')
categorie = soup_categorie[2].text


#Extraction info produit
tds = soup.find_all('class_="table table-striped"' and 'td')
product_information = []
for i in tds:
    valeur_tds = i.text
    product_information.append(valeur_tds)
    

#Création entête + ecriture csv                         
list_livre = {'product_page_url' : URL, 'universal_ product_code (upc)' : product_information[0], 'title' : titre, 'price_including_tax' : product_information[2], 'price_excluding_tax' : product_information[3], 'number_available' : product_information[5], 'product_description' : description, 'category' : categorie, 'review_rating' : product_information[6]}
# entete_csv = ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url')
tableau = pandas.DataFrame(data=[list_livre])#, columns = [entete_csv])
tableau.to_csv('test_2_book.csv')
# print(tableau)


# #Ecriture du CSV
# with open('test_1_book.csv', 'w', newline='', encoding='utf-8') as un_livre:
#     header = ['URL', 'title', 'description', 'categorie', 'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews']
#     writer = csv.DictWriter(un_livre, fieldnames=entete_csv, delimiter=',')
#     writer.writeheader()
#     writer.writerow(dictionnaire_livre)

#     # read_csv


"""

website = 'http://books.toscrape.com/index.html'
URL_livre = 'http://books.toscrape.com/catalogue/chase-me-paris-nights-2_977/index.html'
prefixe_URL = 'http://books.toscrape.com/'


### FONCTIONS

# reponse = requests.get(website)
# soup = BeautifulSoup(reponse.text, 'lxml')
# URL_categorie = []
# prefixe_URL = 'http://books.toscrape.com/'
# # for i in soup.find(class_='side_categories').findChild(class_='nav nav-list').findChild('li').findChild('a'):
# for i in soup.find(class_='side_categories').findChild(class_='nav nav-list').find_next('ul').findChildren('a'):
# # findChild('li').findChildren('a'):
#     # print(i)
#     href_categorie = prefixe_URL + i.get('href')
#     URL_categorie.append(href_categorie)
#     # print(i)
# print(URL_categorie)



response_livre = requests.get(URL_livre)
soup_livre = BeautifulSoup(response_livre.text, 'lxml')
#Extraction de l'image associé
lien_image_partiel = soup_livre.find(id='product_gallery').findChild(class_='item active').findChild('img').get('src')
lien_image_complet = lien_image_partiel.replace("../..", prefixe_URL)
reponse_image = requests.get(lien_image_complet)
image = Image.open(lien_image_complet)
print(reponse_image)

print(lien_image_partiel)
print(lien_image_complet)