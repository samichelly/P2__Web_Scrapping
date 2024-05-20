# PROJECT_2__Web_Scraping

**Project 2 OC: Web Scraping**

## Development Objective

This project was developed to design an ETL (Extract, Transform, Load) pipeline from the website [Books to Scrape](http://books.toscrape.com/index.html). The objective is to extract and analyze data for each book sold by the retailer.

## Development Status

The development is currently complete. However, the following improvements would be welcome:
- **Multiple category selection:** Currently, the program allows scraping either the entire site or a single category. A feature for multiple category selection would be beneficial.
- **Optimization of DataFrames:** Using a single DataFrame instead of two dictionaries with common keys would improve performance.

## Development Environment

The program was developed with Python 3.10 and uses the following packages:
- `beautifulsoup4==4.11.2`
- `bytesbufio==1.0.3`
- `lxml==4.9.2`
- `pandas==1.5.3`
- `Pillow==9.5.0`
- `requests==2.28.2`

## Program Execution

To run the program, follow these steps:

1. **Creating a virtual environment:**
   - Place the `web_scraping_BooksToScrape.py` file and `requirements.txt` in the same folder.
   - In this folder, run the command:
     ```bash
     python3 -m venv env
     ```
   - Activate the virtual environment with:
     - On macOS/Linux:
       ```bash
       source env/bin/activate
       ```
     - On Windows:
       ```bash
       .\env\Scripts\activate
       ```
   - Install the dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Running the program:**
   - Execute the script with the command:
     ```bash
     python .\web_scraping_BooksToScrape.py
     ```
   - Enter the homepage URL of the site when prompted and follow the provided instructions.

3. **Verifying installations:**
   - Use the command:
     ```bash
     pip freeze
     ```
   - to verify that all necessary packages are correctly installed.

## Function Descriptions

The program consists of four main functions:

1. **`parser_page_accueil`:**
   - Lists all categories on the site.
   - Prepares the `URL_categories.csv` file listing the URL links of each category.

2. **`parser_une_categorie`:**
   - Calls `parser_une_page` for each page in the category.
   - Then calls `parser_un_livre` to analyze each book.

3. **`parser_une_page`:**
   - Retrieves the URL links of all books on an HTML page.
   - Returns the results to `parser_une_categorie`.

4. **`parser_un_livre`:**
   - Extracts information related to a book.
   - Transforms and formats the data into a table for CSV export.
   - Downloads images of each book.

## Output Files

All generated elements are stored in an `output` folder, organized by category. Each category contains the extracted images and the corresponding CSV file.
