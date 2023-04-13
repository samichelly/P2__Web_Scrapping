import requests, os, re, csv, pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# website = 'http://books.toscrape.com/index.html'
website = input('\nIndiquez le URL du website à parser : ')
prefixe_URL = 'http://books.toscrape.com/'

### FONCTIONS

# Extraction des categories du website
def categorie_du_site (website):
    reponse = requests.get(website)
    soup = BeautifulSoup(reponse.text, 'lxml')
    URL_categorie = []
    text_categorie = []
    for i in soup.find(class_='side_categories').findChild(class_='nav nav-list').find_next('ul').findChildren('a'):
        count =+ 1
        # print(count)
        href_categorie = prefixe_URL + i.get('href')
        URL_categorie.append(href_categorie)
        text_categorie.append(i.text.strip())
    return(URL_categorie, text_categorie)

#Extraction des URL de livres pour une page
def parser_une_page(URL):
    href_livres_in_page = []
    reponse = requests.get(URL)
    soup = BeautifulSoup(reponse.text, 'lxml')
    for i in soup.find_all(class_='product_pod'):
        for j in i.find_all(class_='image_container'):
            sufixe_URL = j.findChild('a').get('href')
            URL_complet = sufixe_URL.replace("../../..", "http://books.toscrape.com/catalogue")
            href_livres_in_page.append(URL_complet)
    print(f'href_livres_in_page : {href_livres_in_page}')
    return(href_livres_in_page)

#Extraction des URL de livres pour une catégorie
def parser_une_categorie(URL_index):
    reponse = requests.get(URL_index)
    soup = BeautifulSoup(reponse.text, 'lxml')
    nb_page = 0
    entete_csv = ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url')
    tableau = pd.DataFrame(columns = entete_csv)
    href_livres_in_categorie = parser_une_page(URL_index)
    if soup.find(class_="pager"):
        text_pager = soup.find(class_='current').get_text()
        char = text_pager.strip()
        char2 = char.replace("Page 1 of ", "")
        nb_page = int(char2)
        prefixe_URL_index = URL_index.rstrip("index.html")
        for i in range(2,nb_page+1):
            sufixe_URL = ("page-"+str(i)+".html")
            page_suivante = prefixe_URL_index + sufixe_URL
            href_livres_in_categorie = href_livres_in_categorie + parser_une_page(page_suivante)
    print(f'href_livres_in_categorie : {href_livres_in_categorie}')
    for i in href_livres_in_categorie:
        parser_un_livre(i, tableau)  

#Extraction, Transformation, Chargement des informations pour un livre
def parser_un_livre(URL_livre, tableau):
    response_livre = requests.get(URL_livre)
    soup_livre = BeautifulSoup(response_livre.text, 'lxml')
    #Extraction titre
    titre = soup_livre.find(class_="col-sm-6 product_main").h1.text
    #Extraction description
    descript = soup_livre.find(class_="product_page").findChildren('p')
    description = descript[3].text
    if description == '\n\n\n\n\n\n':
        description = 'Pas de desciption disponible'
    #Extraction catégorie
    soup_categorie = soup_livre.find(class_="breadcrumb").findChildren('a')
    categorie = soup_categorie[2].text
    #Extraction informations produit
    tds = soup_livre.find(class_="table table-striped").findChildren('td')
    product_information = []
    for i in tds:
        valeur_tds = i.text
        product_information.append(valeur_tds)
    #Correction infos Prix et Quantité dispo
    prix_Tax = product_information[2].lstrip('Â£')
    prix_HTax = product_information[3].lstrip('Â£')
    quantite_dispo = ''.join(re.findall("[0-9]", product_information[5]))
    #Extraction et enregistrement de l'image
    lien_image_partiel = soup_livre.find(id='product_gallery').findChild(class_='item active').findChild('img').get('src')
    lien_image_complet = lien_image_partiel.replace("../..", prefixe_URL)
    reponse_image = requests.get(lien_image_complet)
    reponse_image = reponse_image.content
    img = Image.open(BytesIO(reponse_image))
    if not os.path.exists(f'output/{categorie}'):
        os.makedirs(f'output/{categorie}')
    image = img.save(f'output/{categorie}/{product_information[0]}.jpg')
    #Extraction Star-rating
    class_star = soup_livre.find(class_="instock availability").find_next('p')
    star_review = class_star['class'][1]
    if star_review == 'One':
        review_rating = 1
    elif star_review == 'Two':
        review_rating = 2
    elif star_review == 'Three':
        review_rating = 3
    elif star_review == 'Four':
        review_rating = 4
    elif star_review == 'Five':
        review_rating = 5
    else :
        review_rating = 0
    list_livre = [URL_livre, product_information[0], titre, prix_Tax, prix_HTax, quantite_dispo, description, categorie, review_rating, lien_image_complet]
    #Remplissage tableau et enregistrement au format CSV
    tableau.loc[len(tableau)] = list_livre
    tableau.to_csv(f'output/{list_livre[-3]}/{list_livre[-3]}.csv', index=None,  sep= ';',  encoding='utf-32')


### CODE PRINCIPAL

retour_data_categorie_du_site = categorie_du_site(website)
URL_categorie = retour_data_categorie_du_site[0]
nom_categorie = retour_data_categorie_du_site[1]

#Enregistrement des URL de chaque catégorie dans un CSV
with open(f'output/URL_categories.csv', 'w', newline='', encoding='utf-8') as extract_categories_to_csv:
    header = ['URL_Categories']
    writer = csv.writer(extract_categories_to_csv)
    writer.writerow(header)
    for i in URL_categorie:
        writer.writerow([i])

#Création dictionnaires pour sélection catégorie à parser
dictionnaire_nom_categorie = {0 : "ANALYSER L'ENSEMBLE DES CATEGORIES"}             #regarder une structure sur 3 colonnes
dictionnaire_URL_categorie = {0 : URL_categorie}
for i, cat_nom in enumerate(nom_categorie):
    dictionnaire_nom_categorie[i+1] = cat_nom
for i, cat_URL in enumerate(URL_categorie):
    dictionnaire_URL_categorie[i+1] = cat_URL
#Choix de la sélection à parser
print("\nIndiquez le numéro de la catégorie à analyser. '0' permet d'analyser l'ensemble du site.\n")
print(f'LES CATEGORIES : \n {dictionnaire_nom_categorie} \n')
selection_categorie = []
selection_categorie = input('Entrez le numéro associé à la catégorie : ')
# selection_categorie = selection_categorie.split(',')
# print(selection_categorie)
selection_categorie = int(selection_categorie)
#Cération de la sélection
if selection_categorie != 0:
    # for i in selection_categorie:
    URL_categorie_selection = [dictionnaire_URL_categorie[selection_categorie]]
    print(URL_categorie_selection)
else:
    URL_categorie_selection = URL_categorie
#Parser la sélection
for i in URL_categorie_selection:
    URL_categorie = parser_une_categorie(i)