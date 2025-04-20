"""
Data Cleaning Utilities

This module provides functions for cleaning and processing laptop data.
"""

import pandas as pd
import re

def clean_data(df):
    """
    Clean and standardize the scraped laptop data.
    
    Args:
        df (pandas.DataFrame): DataFrame containing raw laptop data
    
    Returns:
        pandas.DataFrame: Cleaned DataFrame
    """
    # Create a copy to avoid modifying the original DataFrame
    cleaned_df = df.copy()
    
    # Clean product names
    if 'name' in cleaned_df.columns:
        # Remove extra whitespace
        cleaned_df['name'] = cleaned_df['name'].str.strip()
        # Standardize name format
        cleaned_df['name'] = cleaned_df['name'].apply(standardize_name)
    
    # Clean prices
    if 'price' in cleaned_df.columns:
        # Convert price to float (handle None values)
        cleaned_df['price'] = pd.to_numeric(cleaned_df['price'], errors='coerce')
    
    # Clean ratings
    if 'rating' in cleaned_df.columns:
        # Convert rating to float (handle None values)
        cleaned_df['rating'] = pd.to_numeric(cleaned_df['rating'], errors='coerce')
        # Ensure ratings are on a 5-point scale
        cleaned_df['rating'] = cleaned_df['rating'].apply(standardize_rating)
    
    # Standardize availability
    if 'availability' in cleaned_df.columns:
        cleaned_df['availability'] = cleaned_df['availability'].apply(standardize_availability)
    
    # Drop rows with missing prices
    cleaned_df = cleaned_df.dropna(subset=['price'])
    
    # Reset index
    cleaned_df = cleaned_df.reset_index(drop=True)
    
    return cleaned_df

def combine_data(dataframes_list):
    """
    Combine data from multiple sources into a single DataFrame.
    
    Args:
        dataframes_list (list): List of pandas DataFrames to combine
    
    Returns:
        pandas.DataFrame: Combined DataFrame
    """
    if not dataframes_list:
        return pd.DataFrame()
    
    # Concatenate all DataFrames in the list
    combined_df = pd.concat(dataframes_list, ignore_index=True)
    
    return combined_df

def standardize_name(name):
    """
    Standardize laptop name format.
    
    Args:
        name (str): Laptop name to standardize
    
    Returns:
        str: Standardized laptop name
    """
    if pd.isna(name) or name == "N/A":
        return "Unknown Laptop"
    
    # Remove excessive whitespace
    name = re.sub(r'\s+', ' ', name)
    
    # Capitalize the first letter of each word
    name = name.title()
    
    # Ensure common acronyms remain uppercase
    for acronym in ['SSD', 'HDD', 'RAM', 'GB', 'TB', 'CPU', 'GPU', 'HD', '4K', 'FHD']:
        # Use word boundaries to avoid matching inside words
        name = re.sub(r'\b' + acronym.title() + r'\b', acronym, name, flags=re.IGNORECASE)
    
    return name

def standardize_rating(rating):
    """
    Standardize rating to a 5-point scale.
    
    Args:
        rating (float): Rating to standardize
    
    Returns:
        float: Standardized rating on a 5-point scale
    """
    if pd.isna(rating):
        return None
    
    # If rating is already on a 5-point scale (between 0 and 5)
    if 0 <= rating <= 5:
        return rating
    
    # If rating is on a 10-point scale
    if 0 <= rating <= 10:
        return rating / 2
    
    # If rating is on a 100-point scale (percentage)
    if 0 <= rating <= 100:
        return rating / 20
    
    # For any other scale, return None
    return None

def standardize_availability(availability):
    """
    Standardize availability status.
    
    Args:
        availability (str): Availability status to standardize
    
    Returns:
        str: Standardized availability status
    """
    if pd.isna(availability):
        return "Unknown"
    
    availability = availability.lower()
    
    if any(term in availability for term in ['out of stock', 'épuisé', 'indisponible', 'not available']):
        return "Out of Stock"
    else:
        return "In Stock"