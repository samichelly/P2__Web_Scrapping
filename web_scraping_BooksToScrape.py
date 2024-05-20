import requests
import os
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

prefix_URL = 'http://books.toscrape.com/'

# Extract categories from the website
def parse_home_page(website):
    try:
        response = requests.get(website)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the home page: {e}")
        return [], []

    try:
        soup = BeautifulSoup(response.text, 'lxml')
        category_URLs = []
        category_texts = []
        for i in soup.find(class_='side_categories').findChild(class_='nav nav-list').find_next('ul').findChildren('a'):
            href_category = prefix_URL + i.get('href')
            category_URLs.append(href_category)
            category_texts.append(i.text.strip())
        return category_URLs, category_texts  # category_URLs = URL links, category_texts = Category names
    except Exception as e:
        print(f"Error parsing the home page: {e}")
        return [], []

# Extract book URLs for a page
def parse_one_page(URL):
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []

    try:
        soup = BeautifulSoup(response.text, 'lxml')
        book_urls_per_page = []
        for i in soup.find_all(class_='product_pod'):
            for j in i.find_all(class_='image_container'):
                suffix_URL = j.findChild('a').get('href')
                complete_URL = suffix_URL.replace("../../..", "http://books.toscrape.com/catalogue")
                book_urls_per_page.append(complete_URL)
        print(f'Book URLs per page: {book_urls_per_page}')
        return book_urls_per_page
    except Exception as e:
        print(f"Error parsing the page: {e}")
        return []

# Extract book URLs for a category
def parse_one_category(URL_index):
    try:
        response = requests.get(URL_index)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the category page: {e}")
        return

    try:
        soup = BeautifulSoup(response.text, 'lxml')
        nb_page = 0
        csv_header = (
            'product_page_url', 'universal_product_code (upc)', 'title', 
            'price_including_tax', 'price_excluding_tax', 'number_available', 
            'product_description', 'category', 'review_rating', 'image_url'
        )
        table = pd.DataFrame(columns=csv_header)
        book_urls_per_category = parse_one_page(URL_index)
        if soup.find(class_="pager"):
            text_pager = soup.find(class_='current').get_text()
            nb_page = int(text_pager.strip().split()[-1])
            prefix_URL_index = URL_index.rstrip("index.html")
            for i in range(2, nb_page + 1):
                suffix_URL = f"page-{i}.html"
                next_page = prefix_URL_index + suffix_URL
                book_urls_per_category += parse_one_page(next_page)
        print(f'Book URLs per category: {book_urls_per_category}')
        for book_url in book_urls_per_category:
            parse_one_book(book_url, table)
    except Exception as e:
        print(f"Error parsing the category page: {e}")

# Extract, Transform, Load information for a book
def parse_one_book(book_url, table):
    try:
        response_book = requests.get(book_url)
        response_book.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the book page: {e}")
        return

    try:
        soup_book = BeautifulSoup(response_book.text, 'lxml')
        # Extract title
        title = soup_book.find(class_="col-sm-6 product_main").h1.text
        # Extract description
        description = soup_book.find(class_="product_page").find_all('p')[3].text
        if description == '\n\n\n\n\n\n':
            description = 'No description available'
        # Extract category
        category = soup_book.find(class_="breadcrumb").find_all('a')[2].text
        # Extract product information
        tds = soup_book.find(class_="table table-striped").find_all('td')
        product_information = [td.text for td in tds]
        # Correct price and availability info
        price_tax = product_information[2].lstrip('£')
        price_htax = product_information[3].lstrip('£')
        quantity_available = ''.join(re.findall(r'\d+', product_information[5]))
        # Extract and save image
        partial_image_url = soup_book.find(id='product_gallery').find(class_='item active').find('img').get('src')
        complete_image_url = partial_image_url.replace("../..", prefix_URL)
        response_image = requests.get(complete_image_url).content
        img = Image.open(BytesIO(response_image))
        if not os.path.exists(f'output/{category}'):
            os.makedirs(f'output/{category}')
        img.save(f'output/{category}/{product_information[0]}.jpg')
        # Extract star rating
        star_rating_class = soup_book.find(class_="instock availability").find_next('p')['class'][1]
        review_rating = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }.get(star_rating_class, 0)
        book_data = [
            book_url, product_information[0], title, price_tax, price_htax, 
            quantity_available, description, category, review_rating, complete_image_url
        ]
        # Fill table and save as CSV
        table.loc[len(table)] = book_data
        table.to_csv(f'output/{category}/{category}.csv', index=None, sep=';', encoding='utf-32')
    except Exception as e:
        print(f"Error parsing the book page: {e}")

def main():
    website = input('\nEnter the URL of the website to scrape: ')
    data_parse_home_page = parse_home_page(website)
    category_URLs = data_parse_home_page[0]
    category_names = data_parse_home_page[1]

    # Save category URLs to a CSV
    if not os.path.exists('output'):
        os.makedirs('output')
    try:
        with open('output/URL_categories.csv', 'w', newline='', encoding='utf-8') as extract_categories_to_csv:
            writer = csv.writer(extract_categories_to_csv)
            writer.writerow(['URL_Categories'])
            for url in category_URLs:
                writer.writerow([url])
    except Exception as e:
        print(f"Error writing category URLs to CSV: {e}")

    # Create dictionaries for category selection
    category_name_dict = {i + 1: name for i, name in enumerate(category_names)}
    category_name_dict[0] = "ANALYZE ALL CATEGORIES"
    category_URL_dict = {i + 1: url for i, url in enumerate(category_URLs)}
    category_URL_dict[0] = category_URLs

    # Choose the category to scrape
    print("\nEnter the number of the category to analyze (only one category can be analyzed at a time in this version).\n'0' allows analyzing the entire site.\n")
    print(f'CATEGORIES: \n {category_name_dict} \n')
    try:
        category_selection = int(input('Enter the number associated with the category: '))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    
    # Create the selection
    selected_category_URLs = [category_URL_dict[category_selection]] if category_selection != 0 else category_URLs
    # Parse the selection
    for url in selected_category_URLs:
        parse_one_category(url)

if __name__ == '__main__':
    main()
