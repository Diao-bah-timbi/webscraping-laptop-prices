"""
Data Visualization Utilities

This module provides functions for creating visualizations and 
displaying statistics from laptop price data.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_price_histogram(df, output_path='output/price_distribution.png'):
    """
    Create a histogram of laptop prices.
    
    Args:
        df (pandas.DataFrame): DataFrame containing laptop data
        output_path (str): Path to save the histogram image
    """
    # Set style
    plt.style.use('ggplot')
    
    # Create figure
    plt.figure(figsize=(12, 7))
    
    # Create histogram with price bins
    prices = df['price'].dropna()
    
    if prices.empty:
        plt.text(0.5, 0.5, "No price data available", 
                 horizontalalignment='center', verticalalignment='center',
                 transform=plt.gca().transAxes, fontsize=14)
    else:
        # Determine number of bins based on data range
        price_range = prices.max() - prices.min()
        num_bins = min(30, max(10, int(price_range / 50)))
        
        # Create histogram with custom bins
        n, bins, patches = plt.hist(prices, bins=num_bins, alpha=0.7, color='#4CAF50')
        
        # Add site-specific histograms
        for site in df['site'].unique():
            site_prices = df[df['site'] == site]['price'].dropna()
            if not site_prices.empty:
                plt.hist(site_prices, bins=bins, alpha=0.5, label=site)
        
        # Add mean and median lines
        plt.axvline(prices.mean(), color='red', linestyle='dashed', linewidth=2, label=f'Mean: {prices.mean():.2f}')
        plt.axvline(prices.median(), color='blue', linestyle='dashed', linewidth=2, label=f'Median: {prices.median():.2f}')
    
    # Add labels and title
    plt.xlabel('Price', fontsize=12)
    plt.ylabel('Number of Products', fontsize=12)
    plt.title('Laptop Price Distribution by Site', fontsize=16)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Ensure directory exists and save figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def display_statistics(df):
    """
    Display statistics about the laptop data.
    
    Args:
        df (pandas.DataFrame): DataFrame containing laptop data
    """
    # Check if DataFrame is empty
    if df.empty:
        print("No data available for analysis.")
        return
    
    # Price statistics
    price_stats = df['price'].describe()
    
    print(f"\n{'=' * 40}")
    print("PRICE STATISTICS:")
    print(f"{'=' * 40}")
    print(f"Count:            {price_stats['count']:.0f} laptops")
    print(f"Average Price:    ${price_stats['mean']:.2f}")
    print(f"Median Price:     ${price_stats['50%']:.2f}")
    print(f"Minimum Price:    ${price_stats['min']:.2f}")
    print(f"Maximum Price:    ${price_stats['max']:.2f}")
    print(f"Standard Dev:     ${price_stats['std']:.2f}")
    
    # Rating statistics
    if 'rating' in df.columns and not df['rating'].isna().all():
        rating_stats = df['rating'].describe()
        
        print(f"\n{'=' * 40}")
        print("RATING STATISTICS:")
        print(f"{'=' * 40}")
        print(f"Count:            {rating_stats['count']:.0f} rated laptops")
        print(f"Average Rating:   {rating_stats['mean']:.2f}/5.00")
        print(f"Median Rating:    {rating_stats['50%']:.2f}/5.00")
        print(f"Minimum Rating:   {rating_stats['min']:.2f}/5.00")
        print(f"Maximum Rating:   {rating_stats['max']:.2f}/5.00")
    
    # Site statistics
    print(f"\n{'=' * 40}")
    print("SITE STATISTICS:")
    print(f"{'=' * 40}")
    site_counts = df['site'].value_counts()
    for site, count in site_counts.items():
        print(f"{site}:".ljust(15) + f"{count} laptops")
    
    # Availability statistics
    print(f"\n{'=' * 40}")
    print("AVAILABILITY:")
    print(f"{'=' * 40}")
    availability_counts = df['availability'].value_counts()
    for status, count in availability_counts.items():
        print(f"{status}:".ljust(15) + f"{count} laptops ({count/len(df)*100:.1f}%)")
    
    # Top 5 most expensive laptops
    print(f"\n{'=' * 40}")
    print("TOP 5 MOST EXPENSIVE LAPTOPS:")
    print(f"{'=' * 40}")
    top_expensive = df.sort_values('price', ascending=False).head(5)
    for i, (_, row) in enumerate(top_expensive.iterrows(), 1):
        print(f"{i}. {row['name'][:50]}{'...' if len(row['name']) > 50 else ''}")
        print(f"   Price: ${row['price']:.2f} | Site: {row['site']} | " + 
              (f"Rating: {row['rating']:.1f}/5.0" if not pd.isna(row['rating']) else "Rating: N/A"))
    
    # Top 5 highest rated laptops
    if 'rating' in df.columns and not df['rating'].isna().all():
        print(f"\n{'=' * 40}")
        print("TOP 5 HIGHEST RATED LAPTOPS:")
        print(f"{'=' * 40}")
        top_rated = df.sort_values('rating', ascending=False).head(5)
        for i, (_, row) in enumerate(top_rated.iterrows(), 1):
            print(f"{i}. {row['name'][:50]}{'...' if len(row['name']) > 50 else ''}")
            print(f"   Rating: {row['rating']:.1f}/5.0 | Price: ${row['price']:.2f} | Site: {row['site']}")
    
    # Best value laptops (highest rating/price ratio, for laptops with ratings)
    if 'rating' in df.columns and not df['rating'].isna().all():
        df_with_ratings = df.dropna(subset=['rating'])
        if not df_with_ratings.empty:
            df_with_ratings['value_ratio'] = df_with_ratings['rating'] / df_with_ratings['price']
            
            print(f"\n{'=' * 40}")
            print("TOP 5 BEST VALUE LAPTOPS (RATING/PRICE):")
            print(f"{'=' * 40}")
            best_value = df_with_ratings.sort_values('value_ratio', ascending=False).head(5)
            for i, (_, row) in enumerate(best_value.iterrows(), 1):
                print(f"{i}. {row['name'][:50]}{'...' if len(row['name']) > 50 else ''}")
                print(f"   Value: {row['value_ratio']*100:.2f} | Rating: {row['rating']:.1f}/5.0 | " +
                      f"Price: ${row['price']:.2f} | Site: {row['site']}")