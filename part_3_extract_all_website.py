import requests, os, re, csv, pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

website = 'http://books.toscrape.com/index.html'
# URL = ['http://books.toscrape.com/catalogue/category/books/romance_8/index.html', 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html']
href_livres_in_categorie = []
prefixe_URL = 'http://books.toscrape.com/'
new_url = []
### FONCTIONS

# Extraction des categories de BooksToscrape
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
    # creation_dataframe_par_categorie(text_categorie)
    return(URL_categorie, text_categorie)

def creation_dataframe_par_categorie(text_categorie):
    liste_nom_categorie = text_categorie
    tableaux = {}
    entete_csv = ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url')
    for categorie_tableau in liste_nom_categorie:
        # dataframe_categorie = pd.DataFrame(columns = entete_csv)
        tableaux[categorie_tableau] = pd.DataFrame(columns = entete_csv)
    # print(type(dataframe_categorie))
    # print({dataframe_categorie})
    return(tableaux)

#Extraction des URL de livres pour une page de catégorie
def listes_livres_par_categorie(URL):
    reponse = requests.get(URL)
    soup = BeautifulSoup(reponse.text, 'lxml')
    for i in soup.find_all(class_='product_pod'):
        for j in i.find_all(class_='image_container'):
            sufixe_URL = j.findChild('a').get('href')
            URL_complet = sufixe_URL.replace("../../..", "http://books.toscrape.com/catalogue")
            href_livres_in_categorie.append(URL_complet)
    return(href_livres_in_categorie)

#Création des pages de catégorie suivants l'index (page 1)
def traitement_pour_plusieurs_pages_par_categorie(URL):
    reponse = requests.get(URL)
    soup = BeautifulSoup(reponse.text, 'lxml')
    nb_page = 0
    if soup.find(class_="pager"):
        text_pager = soup.find(class_='current').get_text()
        char = text_pager.strip()
        char2 = char.replace("Page 1 of ", "")
        nb_page = int(char2)
    for i in range(1,nb_page):
        prefixe_URL = URL.rstrip("index.html")
        sufixe_URL = ("page-"+str(i+1)+".html")
        page_suivante = prefixe_URL + sufixe_URL
        new_url.append(page_suivante)
    return(new_url)

#Extraction des informations pour un livre
def parser_un_livre(URL_livre, tableau):                           #ajouter tableau en paramètre ou argument de base none (conditions)
    response_livre = requests.get(URL_livre)
    soup_livre = BeautifulSoup(response_livre.text, 'lxml')
    #Extraction titre OK
    titre = soup_livre.find(class_="col-sm-6 product_main").h1.text
    #Extraction description OK
    descript = soup_livre.find(class_="product_page").findChildren('p')
    description = descript[3].text
    if description == '\n\n\n\n\n\n':
        description = 'Pas de desciption disponible'
    #Extraction catégorie OK
    soup_categorie = soup_livre.find(class_="breadcrumb").findChildren('a')
    categorie = soup_categorie[2].text
    #Extraction info produit
    tds = soup_livre.find(class_="table table-striped").findChildren('td')
    product_information = []
    for i in tds:
        valeur_tds = i.text
        product_information.append(valeur_tds)
    #Correction info Prix et Quantité dispo
    prix_Tax = product_information[2].lstrip('Â£')
    prix_HTax = product_information[3].lstrip('Â£')
    quantite_dispo = ''.join(re.findall("[0-9]", product_information[5]))
    #Extraction de l'image associé
    lien_image_partiel = soup_livre.find(id='product_gallery').findChild(class_='item active').findChild('img').get('src')
    lien_image_complet = lien_image_partiel.replace("../..", prefixe_URL)
    #Enregistrement image de livre
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
    """
    for i in tableau:
        tableau[i] = pd.DataFrame(tableau[i])
    # tableau_analyse = pd.DataFrame(tableau[i])
    print(tableau[i])
    for i in tableau.keys():
        if i == list_livre[-3]:
            # print(i)
            # print(list_livre[-3])
            i = pd.DataFrame(tableau[i])
            # print(i)
            i.loc[len(i)] = list_livre
            # print(i)
        # else:
            # print("Est différent")
        # print(f'Tableau parser_un_livre {i}')
    """
    return(list_livre)


### CODE PRINCIPAL

entete_csv = ('product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url')
retour_data_categorie_du_site = categorie_du_site(website)
# print(categorie_du_site(website))
URL_categorie = retour_data_categorie_du_site[0]
nom_categorie = retour_data_categorie_du_site[1]

with open(f'output/Extract_categories.csv', 'w', newline='', encoding='utf-8') as extract_categories_to_csv:
    header = ['URL_Categories']
    writer = csv.writer(extract_categories_to_csv)
    writer.writerow(header)
    for i in URL_categorie:
        writer.writerow([i])


dictionnaire_nom_categorie = {0 : "ANALYSER L'ENSEMBLE DES CATEGORIES"}
dictionnaire_URL_categorie = {0 : URL_categorie}
for i, cat_nom in enumerate(nom_categorie):
    dictionnaire_nom_categorie[i+1] = cat_nom
for i, cat_URL in enumerate(URL_categorie):
    dictionnaire_URL_categorie[i+1] = cat_URL
print(f'LES CATEGORIES : \n {dictionnaire_nom_categorie} \n')
selection_categorie = []
selection_categorie = input('Entrez le numéro associé à la catégorie : ')
selection_categorie = int(selection_categorie)
if selection_categorie != 0:
    URL_categorie_selection = [dictionnaire_URL_categorie[selection_categorie]]
else:
    URL_categorie_selection = URL_categorie
for i in URL_categorie_selection:
    URL_complement = traitement_pour_plusieurs_pages_par_categorie(i)
    URL_categorie = URL_categorie_selection + URL_complement

print(f'URL categorie selection : {URL_categorie_selection}')
print(f'URL complement : {URL_complement}')
print(f'URL categorie : {URL_categorie}')

for i in URL_categorie:
    href_categorie = listes_livres_par_categorie(i)
print(len(href_categorie))


tableau = creation_dataframe_par_categorie(nom_categorie)
# print(tableau.keys())
for i in href_categorie:
    liste_livre = parser_un_livre(i, tableau)
    # print(liste_livre)

#     tableau.loc[len(tableau)] = liste_livre
#     categorie_dossier = liste_livre[-3]
#     # print(categorie_dossier)
# # print(tableau)
# for categorie_dataframe, group in tableau.groupby('category'):
#     group.to_csv(f'output/{categorie_dossier}/{categorie_dataframe}.csv', index=None,  sep= ';',  encoding='utf-32')
