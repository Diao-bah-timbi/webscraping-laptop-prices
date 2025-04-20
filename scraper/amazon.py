"""
Amazon Laptop Scraper Module

This module scrapes laptop data from Amazon.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_amazon(limit=20):
    """
    Scrape laptop information from Amazon.
    
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
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    # URL for Amazon laptops search
    url = "https://www.amazon.com/s?k=laptop&i=computers&rh=n%3A565108"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all product containers
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        # Limit the number of products to scrape
        products = products[:min(len(products), limit)]
        
        for product in products:
            # Extract product name
            name_element = product.find('span', {'class': 'a-size-medium'})
            if not name_element:
                name_element = product.find('h2', {'class': 'a-size-mini'})
            
            name = name_element.text.strip() if name_element else "N/A"
            names.append(name)
            
            # Extract price
            price_element = product.find('span', {'class': 'a-price-whole'})
            if price_element:
                price_fraction = product.find('span', {'class': 'a-price-fraction'})
                price = float(price_element.text.replace(',', '') + 
                             (price_fraction.text if price_fraction else '.00'))
            else:
                price = None
            prices.append(price)
            
            # Extract rating
            rating_element = product.find('span', {'class': 'a-icon-alt'})
            if rating_element and 'out of 5 stars' in rating_element.text:
                rating = float(rating_element.text.split(' ')[0])
            else:
                rating = None
            ratings.append(rating)
            
            # Extract availability
            availability_element = product.find('span', {'class': 'a-color-price'})
            availability = "In Stock"
            if availability_element and "out of stock" in availability_element.text.lower():
                availability = "Out of Stock"
            availabilities.append(availability)
            
            # Add a small delay to avoid being blocked
            time.sleep(random.uniform(0.1, 0.3))
        
        # Create a DataFrame with the scraped data
        data = {
            'name': names,
            'price': prices,
            'rating': ratings,
            'availability': availabilities,
            'site': ['Amazon'] * len(names)
        }
        
        return pd.DataFrame(data)
    
    except requests.RequestException as e:
        print(f"Error during Amazon scraping: {e}")
        # Return empty DataFrame in case of error
        return pd.DataFrame({
            'name': [],
            'price': [],
            'rating': [],
            'availability': [],
            'site': []
        })