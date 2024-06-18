

# Web Scraping

## Summary

This project consists of two Python scripts: `datascapping.py` and `login.py`. 

- **datascapping.py**: Scrapes product information from Amazon using requests and BeautifulSoup. It logs scraping activities to `amazon_scraper.log` and saves the extracted data to `amazon_product_data.csv`.
  
- **login.py**: Automates the login process to Stack Overflow using Selenium WebDriver. It logs activities to `automation.log` and requires credentials provided in the `.env` file.

## Installation of Necessary Imports

Before running the scripts, ensure you have the necessary Python packages installed. You can install them using pip:

```bash
pip install requests beautifulsoup4 selenium python-dotenv
```


## Commands to Clone the Repo

To clone this repository and run the scripts, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/purvaac/automation.git
   cd automation
   ```


## Usage

### datascapping.py

Ensure you have `requests` and `beautifulsoup4` installed:

```bash
pip install requests beautifulsoup4
```

Run the script using Python:

```bash
python datascapping.py
```

### login.py

Ensure you have `selenium` and `python-dotenv` installed:

```bash
pip install selenium python-dotenv
```

Run the script using Python:

```bash
python login.py
```

