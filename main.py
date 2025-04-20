#!/usr/bin/env python3
"""
Laptop Price Scraper and Analyzer - Main Entry Point

This script coordinates the scraping of laptop prices from multiple e-commerce sites,
processes the data, and generates visualizations and analysis.
"""

import os
import argparse
from datetime import datetime

from scraper.amazon import scrape_amazon
from scraper.cdiscount import scrape_cdiscount
from scraper.boulanger import scrape_boulanger
from utils.data_cleaning import clean_data, combine_data
from utils.visualizer import create_price_histogram, display_statistics

def main():
    """Main function to run the laptop price scraper and analyzer."""
    
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Scrape and analyze laptop prices from e-commerce sites')
    parser.add_argument('--sites', nargs='+', choices=['amazon', 'cdiscount', 'boulanger', 'all'], 
                        default=['all'], help='Sites to scrape (default: all)')
    parser.add_argument('--min-price', type=float, help='Minimum price filter')
    parser.add_argument('--max-price', type=float, help='Maximum price filter')
    parser.add_argument('--min-rating', type=float, help='Minimum rating filter (1-5)')
    parser.add_argument('--limit', type=int, default=20, help='Limit number of products per site (default: 20)')
    parser.add_argument('--output', type=str, default='laptops.csv', help='Output CSV filename')
    args = parser.parse_args()
    
    print(f"\n{'=' * 60}")
    print(f"🔍 LAPTOP PRICE SCRAPER AND ANALYZER")
    print(f"{'=' * 60}")
    print(f"⏱️  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Determine which sites to scrape
    sites_to_scrape = []
    if 'all' in args.sites or 'amazon' in args.sites:
        sites_to_scrape.append(('Amazon', scrape_amazon))
    if 'all' in args.sites or 'cdiscount' in args.sites:
        sites_to_scrape.append(('Cdiscount', scrape_cdiscount))
    if 'all' in args.sites or 'boulanger' in args.sites:
        sites_to_scrape.append(('Boulanger', scrape_boulanger))
    
    # Scrape data from each site
    all_data = []
    for site_name, scrape_func in sites_to_scrape:
        print(f"\n📊 Scraping {site_name}...")
        try:
            site_data = scrape_func(limit=args.limit)
            print(f"✅ Found {len(site_data)} products on {site_name}")
            all_data.append(site_data)
        except Exception as e:
            print(f"❌ Error scraping {site_name}: {e}")
    
    if not all_data:
        print("\n❌ No data was scraped. Exiting.")
        return
    
    # Combine and clean data
    print("\n🧹 Cleaning and combining data...")
    combined_df = combine_data(all_data)
    cleaned_df = clean_data(combined_df)
    
    # Apply filters if specified
    filtered_df = cleaned_df.copy()
    filter_applied = False
    
    if args.min_price is not None:
        filtered_df = filtered_df[filtered_df['price'] >= args.min_price]
        filter_applied = True
    
    if args.max_price is not None:
        filtered_df = filtered_df[filtered_df['price'] <= args.max_price]
        filter_applied = True
    
    if args.min_rating is not None:
        filtered_df = filtered_df[filtered_df['rating'] >= args.min_rating]
        filter_applied = True
    
    if filter_applied:
        print(f"🔍 Applied filters: {len(filtered_df)} products remaining")
    
    # Save to CSV
    output_path = os.path.join('output', args.output)
    filtered_df.to_csv(output_path, index=False)
    print(f"\n💾 Data saved to {output_path}")
    
    # Generate visualizations
    if not filtered_df.empty:
        print("\n📈 Generating visualizations...")
        histogram_path = os.path.join('output', 'price_distribution.png')
        create_price_histogram(filtered_df, output_path=histogram_path)
        print(f"📊 Price histogram saved to {histogram_path}")
        
        # Display statistics
        print("\n📊 Data Analysis Summary:")
        display_statistics(filtered_df)
    else:
        print("\n⚠️ No data after filtering. Cannot generate visualizations.")
    
    print(f"\n✅ Process completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    main()