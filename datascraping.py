import csv
import logging
import time
import random
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError

# Configure logging
logging.basicConfig(filename='amazon_scraper.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    # Add Safari user agent
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1'
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

#Scrapes product information from Amazon
def scrape_amazon_product(url):
    headers = {'User-Agent': get_random_user_agent()}
    try:
        logging.debug("Sending request to URL: %s with headers: %s", url, headers)
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        logging.debug("Received response from URL: %s", url)
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('span', id='productTitle')
        title = title_tag.get_text().strip() if title_tag else 'Title not available'
        logging.debug("Extracted title: %s", title)

        # Extract price
        price = 'Price not available'
        try:
            # Modify here to extract the price
            price_element = soup.find('span', class_='a-price-whole')
            price = price_element.get_text().strip() if price_element else 'Price not available'
            logging.debug("Extracted price: %s", price)
        except Exception as e:
            logging.error("Error extracting price: %s", e)


        # Extract reviews data
        reviews_data = []
        try:
            review_sections = soup.find_all('div', {'data-hook': 'review'})
            for review_section in review_sections:
                review = {}
                review['title'] = review_section.find('a', {'data-hook': 'review-title'}).get_text().strip()
                review['rating'] = review_section.find('i', {'data-hook': 'review-star-rating'}).get_text().strip().split()[0]
                review['text'] = review_section.find('span', {'data-hook': 'review-body'}).get_text().strip()
                reviews_data.append(review)
            logging.debug("Extracted reviews data: %s", reviews_data)
        except Exception as e:
            logging.error("Error extracting reviews data: %s", e)

        product_data = {
            'title': title,
            'price': price,
            'reviews': reviews_data
        }

        logging.debug("Product data extracted: %s", product_data)
        return product_data

    except HTTPError as http_err:
        logging.error("HTTP error occurred: %s", http_err)
    except Exception as err:
        logging.error("An error occurred while scraping the product: %s", err)
    return None

def save_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'price',  'reviews'])
            writer.writeheader()
            writer.writerow(data)
            logging.debug("Data written to CSV file: %s", filename)
    except Exception as e:
        logging.error("File error: %s", e)

if __name__ == "__main__":
    url = "https://www.amazon.in/gp/aw/d/B0CHXDVMVP/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=a945c770ceff805a4b90ee62cb5ae580&hsa_cr_id=0&qid=1718216860&sr=1-1-e0fa1fdd-d857-4087-adda-5bd576b25987&ref_=sbx_be_s_sparkle_mcd_asin_0_img&pd_rd_w=B1Ucc&content-id=amzn1.sym.df9fe057-524b-4172-ac34-9a1b3c4e647d%3Aamzn1.sym.df9fe057-524b-4172-ac34-9a1b3c4e647d&pf_rd_p=df9fe057-524b-4172-ac34-9a1b3c4e647d&pf_rd_r=1FKYQ0BDZGESTFCDY2GH&pd_rd_wg=MuRbi&pd_rd_r=96796d04-92f5-435e-9006-fe19bb9f0764"
    
    retries = 5
    for attempt in range(retries):
        product_data = scrape_amazon_product(url)
        if product_data:
            save_to_csv(product_data, 'amazon_product_data.csv')
            break
        else:
            logging.debug("Retrying... Attempt %d of %d", attempt + 1, retries)
            time.sleep(2 ** attempt + random.uniform(0, 1))  # Exponential backoff with random delay
    else:
        logging.error("Failed to scrape product data after %d attempts", retries)
