"""
Cdiscount Laptop Scraper Module

This module scrapes laptop data from Cdiscount.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_cdiscount(limit=20):
    """
    Scrape laptop information from Cdiscount.
    
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "DNT": "1"
}

    
    # URL for Cdiscount laptops search
    url = "https://www.cdiscount.com/search/10/ordinateur+portable.html"

    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all product containers
        products = soup.find_all('li', {'class': 'pbElementLi'})
        
        # Limit the number of products to scrape
        products = products[:min(len(products), limit)]
        
        for product in products:
            # Extract product name
            name_element = product.find('div', {'class': 'prdtBTit'})
            name = name_element.text.strip() if name_element else "N/A"
            names.append(name)
            
            # Extract price
            price_element = product.find('span', {'class': 'price'})
            if price_element:
                # Replace comma with dot for decimal separator and remove currency symbol
                price_text = price_element.text.strip().replace('€', '').replace(',', '.').strip()
                try:
                    price = float(price_text)
                except ValueError:
                    price = None
            else:
                price = None
            prices.append(price)
            
            # Extract rating
            rating_element = product.find('div', {'class': 'prdtBILRate'})
            if rating_element:
                # Convert rating from percentage to 5-star scale
                style = rating_element.get('style', '')
                if 'width' in style:
                    try:
                        width_percentage = float(style.split(':')[1].replace('%', '').strip())
                        rating = (width_percentage / 100) * 5
                    except (ValueError, IndexError):
                        rating = None
                else:
                    rating = None
            else:
                rating = None
            ratings.append(rating)
            
            # Extract availability
            availability_element = product.find('div', {'class': 'availStat'})
            if availability_element and "épuisé" in availability_element.text.lower():
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
            'site': ['Cdiscount'] * len(names)
        }
        
        return pd.DataFrame(data)
    
    except requests.RequestException as e:
        print(f"Error during Cdiscount scraping: {e}")
        # Return empty DataFrame in case of error
        return pd.DataFrame({
            'name': [],
            'price': [],
            'rating': [],
            'availability': [],
            'site': []
        })