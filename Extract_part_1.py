import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import pandas

#def parser_one_book(URL):

#Récupérer le contenu de la page HTML + création objet Soup OK
URL = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'lxml')

#Extraction titre OK
titre = soup.find(class_="col-sm-6 product_main").h1.text

#Extraction description OK
descript = soup.find_all('class_="product_page"' and 'p')
description = descript[3].text

#Extraction catégorie OK
soup_categorie = soup.find_all('class_="breadcrumb"' and 'a')
categorie = soup_categorie[3].text

#Extraction info produit
ths = soup.find_all('class_="table table-striped"' and 'th')
tds = soup.find_all('class_="table table-striped"' and 'td')

dictionnaire_livre = {'URL' : URL, 'title' : titre, 'description' : description, 'categorie' : categorie}
for i, j in zip(ths, tds):
    valeur_ths = i.text     # attention pour plusieurs livres (prendre les ths 1 seule fois)
    valeur_tds = j.text
    dictionnaire_livre[valeur_ths] = valeur_tds


print(dictionnaire_livre)


#Ecriture du CSV
with open('test_1_book.csv', 'w', newline='', encoding='utf-8') as un_livre:
    header = ['URL', 'title', 'description', 'categorie', 'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews']
    #['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    writer = csv.DictWriter(un_livre, fieldnames=header, delimiter=',')
    writer.writeheader()
    writer.writerow(dictionnaire_livre)

    # read_csv
