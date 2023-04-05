import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import pandas

#def parser_one_book(URL):

#Récupérer le contenu de la page HTML + création objet Soup OK
URL = ['http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', 'http://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html']
tableau = pandas.DataFrame()
list_livre = []


def parser_un_livre(URL):                           #ajouter tableau en paramètre ou argument de base none (conditions)
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')

    #Extraction titre OK
    titre = soup.find(class_="col-sm-6 product_main").h1.text

    #Extraction description OK
    descript = soup.find_all('class_="product_page"' and 'p')
    description = descript[3].text
    # print(description)

    #Extraction catégorie OK
    soup_categorie = soup.find_all('class_="breadcrumb"' and 'a')
    categorie = soup_categorie[3].text

    #Extraction info produit
    tds = soup.find_all('class_="table table-striped"' and 'td')
    product_information = []
    for i in tds:
        valeur_tds = i.text
        product_information.append(valeur_tds)
    list_livre = [URL, product_information[0], titre, product_information[2], product_information[3], product_information[5], description, categorie, product_information[6]]   
    return(list_livre)




# 2 fonctions
# 1ere créer + ajouter data 
# 2eme dataframe to csv


#     #Création tableau récap                           #2 parties : créer le tableau + ajouter data (avec if)          /// utiliser une list[]
#     list_livre = {'product_page_url' : URL, 'universal_ product_code (upc)' : product_information[0], 'title' : titre, 'price_including_tax' : product_information[2], 'price_excluding_tax' : product_information[3], 'number_available' : product_information[5], 'product_description' : description, 'category' : categorie, 'review_rating' : product_information[6]}    
# # entete_csv = ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url')
#     livre = pandas.DataFrame(data=[list_livre]) #, columns = [entete_csv])
#     tableau = livre.concat(list_livre, ignore_index=True)                 concat à enlever -> ajouter une ligne
#     
# 
# 
# return(tableau)

# Main
count= 0
entete_csv = ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating')
for i in URL:
    parser_un_livre(i)
    liste_livre = parser_un_livre(URL=i)
    count +=1
    print(count)
    if count == 1 :
        tableau = pandas.DataFrame(columns = entete_csv)
        tableau.loc[count] = liste_livre
        print(tableau)
    else:
        tableau.loc[count] = liste_livre
        print(tableau)

# Création tableau récap   

# print(liste_livre)
# livre = pandas.DataFrame(columns = entete_csv)
# print(livre)


# tableau = livre.concat(list_livre, ignore_index=True)
    
# tableau.to_csv('test_2_book.csv')

