"""
Boulanger Laptop Scraper Module

This module scrapes laptop data from Boulanger.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_boulanger(limit=20):
    """
    Scrape laptop information from Boulanger.
    
    Args:
        limit (int): Maximum number of products to scrape
    
    Returns:
        pandas.DataFrame: DataFrame containing laptop data
    """
    # Create empty lists to store data
    names = []
    prices = []
    ratings = []
    availabilities = []
    
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    # URL for Boulanger laptops search
    url = "https://www.boulanger.com/c/ordinateur-portable-bureau"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all product containers
        products = soup.find_all('div', {'class': 'product-list__item'})
        
        # Limit the number of products to scrape
        products = products[:min(len(products), limit)]
        
        for product in products:
            # Extract product name
            name_element = product.find('h2', {'class': 'product-title'})
            name = name_element.text.strip() if name_element else "N/A"
            names.append(name)
            
            # Extract price
            price_element = product.find('div', {'class': 'price'})
            if price_element:
                # Extract the numerical price and convert to float
                price_text = price_element.text.strip().replace('€', '').replace(',', '.').strip()
                try:
                    price = float(price_text)
                except ValueError:
                    price = None
            else:
                price = None
            prices.append(price)
            
            # Extract rating
            rating_element = product.find('span', {'class': 'rating-value'})
            if rating_element:
                try:
                    rating = float(rating_element.text.strip().replace(',', '.'))
                except ValueError:
                    rating = None
            else:
                rating = None
            ratings.append(rating)
            
            # Extract availability
            availability_element = product.find('div', {'class': 'availability'})
            if availability_element and "indisponible" in availability_element.text.lower():
                availability = "Out of Stock"
            else:
                availability = "In Stock"
            availabilities.append(availability)
            
            # Add a small delay to avoid being blocked
            time.sleep(random.uniform(0.1, 0.3))
        
        # Create a DataFrame with the scraped data
        data = {
            'name': names,
            'price': prices,
            'rating': ratings,
            'availability': availabilities,
            'site': ['Boulanger'] * len(names)
        }
        
        return pd.DataFrame(data)
    
    except requests.RequestException as e:
        print(f"Error during Boulanger scraping: {e}")
        # Return empty DataFrame in case of error
        return pd.DataFrame({
            'name': [],
            'price': [],
            'rating': [],
            'availability': [],
            'site': []
        })