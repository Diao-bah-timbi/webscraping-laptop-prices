# Laptop Price Scraper and Analyzer

A Python tool for scraping laptop prices from multiple e-commerce websites, analyzing the data, and generating visualizations.

## Features

- Multi-site scraping from Amazon, Cdiscount, and Boulanger
- Data cleaning and standardization
- CSV export of scraped data
- Visual analysis with price histograms
- Statistical analysis with price and rating metrics
- Command-line interface with filtering options

## Requirements

- Python 3.6+
- Required packages (listed in `requirements.txt`):
  - requests
  - beautifulsoup4
  - pandas
  - matplotlib
  - argparse
  - lxml

## Installation

1. Clone this repository:
```
git clone <repository-url>
```

2. Navigate to the project directory:
```
cd laptop-price-scraper
```

3. Install required packages:
```
pip install -r requirements.txt
```

## Usage

### Basic Usage

To scrape all supported sites with default settings:

```
python main.py
```

### Advanced Options

```
python main.py --sites amazon cdiscount --min-price 500 --max-price 1200 --min-rating 4.0 --limit 30 --output laptops_filtered.csv
```

### Command-line Arguments

- `--sites`: Sites to scrape (choices: amazon, cdiscount, boulanger, all) [default: all]
- `--min-price`: Minimum price filter
- `--max-price`: Maximum price filter
- `--min-rating`: Minimum rating filter (1-5)
- `--limit`: Limit number of products per site [default: 20]
- `--output`: Output CSV filename [default: laptops.csv]

## Output

The script generates:

1. A CSV file with all scraped data (`output/laptops.csv` by default)
2. A price distribution histogram (`output/price_distribution.png`)
3. A statistical analysis displayed in the terminal

## Project Structure

```
laptop-price-scraper/
├── main.py                 # Main entry point
├── requirements.txt        # Package dependencies
├── README.md               # This documentation
├── scraper/
│   ├── __init__.py
│   ├── amazon.py           # Amazon scraper
│   ├── cdiscount.py        # Cdiscount scraper
│   └── boulanger.py        # Boulanger scraper
├── utils/
│   ├── __init__.py
│   ├── data_cleaning.py    # Data cleaning utilities
│   └── visualizer.py       # Visualization utilities
└── output/                 # Generated output (created on first run)
    ├── laptops.csv
    └── price_distribution.png
```

## Notes

- This tool is for educational purposes only
- Please respect the terms of service of the websites you scrape
- Add delays between requests to avoid being blocked
- Some websites may change their structure, requiring updates to the scrapers

## License

MIT License