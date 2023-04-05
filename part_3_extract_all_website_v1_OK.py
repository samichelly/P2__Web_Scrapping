import requests
from bs4 import BeautifulSoup
import csv
import pandas

website = 'http://books.toscrape.com/index.html'
URL = ['http://books.toscrape.com/catalogue/category/books/romance_8/index.html', 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html']
href_livres_in_categorie = []
# new_url = []


### FONCTIONS

def categorie_du_site (website):
    reponse = requests.get(website)
    soup = BeautifulSoup(reponse.text, 'lxml')
    URL_categorie = []
    prefixe_URL = 'http://books.toscrape.com/'
    # for i in soup.find(class_='side_categories').findChild(class_='nav nav-list').findChild('li').findChild('a'):
    for i in soup.find(class_='side_categories').findChild(class_='nav nav-list').find_next('ul').findChildren('a'):
    # findChild('li').findChildren('a'):
        href_categorie = prefixe_URL + i.get('href')
        URL_categorie.append(href_categorie)
        # print(i)
    print(URL_categorie)
    return(URL_categorie)


#Extraction des URL de livres pour une page de catégorie
def listes_livres_par_categorie(URL):
    reponse = requests.get(URL)
    soup = BeautifulSoup(reponse.text, 'lxml')
    for i in soup.find_all(class_='product_pod'):              
        # print(i)
        for j in i.find_all(class_='image_container'):               #renforcer la sélection avec l'ensemble au-dessus
            sufixe_URL = j.findChild('a').get('href')
            # print(sufixe_URL)
            URL_complet = sufixe_URL.replace("../../..", "http://books.toscrape.com/catalogue")
            href_livres_in_categorie.append(URL_complet)
            # print(URL_complet)
    return(href_livres_in_categorie)

#Création des pages de catégorie suivants l'index (page 1)
def traitement_pour_plusieurs_pages_par_categorie(URL):
    reponse = requests.get(URL)
    soup = BeautifulSoup(reponse.text, 'lxml')
    nb_page = 0
    char2 = ''
    if soup.find(class_="pager"):
# Première idée - sélectionné le ou les 2 derniers nombre pour boucler dessus
        # text_pager = soup.find(class_='current').get_text()
        # char2 = text_pager.strip()
        # char3 = char2[-1]
        # print(text_pager)
        # print(char2)
        # print(len(char2))
        # print(char3)
        # nb_page = int(char3)
        # print(nb_page)
        # print(type(nb_page))
# Seconde idée - supprimé le début de la chaîne pour garder le ou les nombres pour boucler dessus
        text_pager = soup.find(class_='current').get_text()
        char = text_pager.strip()
        char2 = char.replace("Page 1 of ", "")
        # print(text_pager)
        # print(char2)
        # print(len(char2))
        nb_page = int(char2)            #Conversion du string en int pour boucle for suivante
        # print(nb_page)
        # print(type(nb_page))
    else:
        ()
    new_url = []
    # for i in range(nb_page-1):    #struture erreur for i in nb_page:, corrigé
    #     # if i != 0:
    #         prefixe_URL = URL.rstrip("index.html")
    #         sufixe_URL = ("page-"+str(i+2)+".html")
    #         page_suivante = prefixe_URL + sufixe_URL
    #         # print(URL)
    #         # print(type(new_url))
    #         # print(page_suivante)
    #         # print(type(page_suivante))
    #         new_url.append(page_suivante)
    #     # if i == 0:
    #         # print("Verif i == 0")
    #         # ()
    # else:
    #     ()
    # print(new_url)
    for i in range(1,nb_page):    #struture erreur for i in nb_page:, corrigé
    # if i != 0:
        prefixe_URL = URL.rstrip("index.html")
        sufixe_URL = ("page-"+str(i+1)+".html")
        page_suivante = prefixe_URL + sufixe_URL
        # print(URL)
        # print(type(new_url))
        # print(page_suivante)
        # print(type(page_suivante))
        new_url.append(page_suivante)
    # if i == 0:
        # print("Verif i == 0")
        # ()
    else:
        ()
    # print(new_url)
    return(new_url)

#Extraction des informations pour un livre
def parser_un_livre(URL_livre):                           #ajouter tableau en paramètre ou argument de base none (conditions)
    response_livre = requests.get(URL_livre)
    soup_livre = BeautifulSoup(response_livre.text, 'lxml')
    #Extraction titre OK
    titre = soup_livre.find(class_="col-sm-6 product_main").h1.text
    #Extraction description OK
    descript = soup_livre.find(class_="product_page").findChildren('p')
    description = descript[3].text
    #Extraction catégorie OK
    soup_categorie = soup_livre.find(class_="breadcrumb").findChildren('a')
    categorie = soup_categorie[2].text
    #Extraction info produit
    tds = soup_livre.find(class_="table table-striped").findChildren('td')
    product_information = []
    for i in tds:
        valeur_tds = i.text
        product_information.append(valeur_tds)
    list_livre = [URL_livre, product_information[0], titre, product_information[2], product_information[3], product_information[5], description, categorie, product_information[6]]
    return(list_livre)


### CODE PRINCIPAL

count= 0
entete_csv = ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating')
URL_categorie = categorie_du_site(website)
for i in URL_categorie:
    # URL_categorie.append(i)
    URL_complement = traitement_pour_plusieurs_pages_par_categorie(i)
    # print(URL_complement)
    # URL_categorie.append(URL_complement)                          #crée des listes dans la listes, problème
    URL_categorie = URL_categorie + URL_complement
# print(URL_categorie)

for i in URL_categorie:
    href_categorie = listes_livres_par_categorie(i)
    # print(i)
    # print(href_categorie)
    # href_categorie.clear()
# print(href_categorie)
# print(len(href_categorie))
for i in href_categorie:
    liste_livre = parser_un_livre(i)
    count +=1
    if count == 1 :
        tableau = pandas.DataFrame(columns = entete_csv)
        tableau.loc[count] = liste_livre
    else:
        tableau.loc[count] = liste_livre
print(tableau)
tableau.to_csv('test_2_book.csv', encoding='utf-8')



