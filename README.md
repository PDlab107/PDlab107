# John Pye Auction Profit Analyzer

An automated tool that searches John Pye auctions for automotive parts, compares prices with eBay sold listings, and identifies profitable opportunities.

## Features

- **Automated Auction Search**: Searches John Pye auctions for a predefined list of automotive brands and manufacturers
- **Part Number & Brand Extraction**: Automatically extracts part numbers and brand names from auction titles
- **Price Comparison**: Compares current auction prices with recent eBay sold listings for similar items
- **Profit Analysis**: Calculates profit margins accounting for auction fees (1.5x multiplier)
- **Smart Highlighting**: Identifies items that meet either >50% profit margin OR >£50 profit threshold
- **Sorted Results**: Results sorted by auction end time with soonest auctions at the top
- **CSV Export**: Exports all data to CSV format for easy analysis

## Requirements

- Python 3.7+
- Chrome browser (for Selenium WebDriver)
- Internet connection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/PDlab107/PDlab107.git
cd PDlab107
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python auction_search_app_nobosch.py
```

The script will:
1. Search John Pye auctions for each brand in the configured list
2. Extract auction details (title, part number, make, current bid, end time)
3. Look up comparable prices on eBay sold listings
4. Calculate profit margins accounting for fees
5. Save results to `auction_results/bosch_lots.csv`

## Output Format

The CSV output includes:
- **Link**: Direct link to the auction listing
- **Title**: Full auction title
- **Part Number**: Extracted part number
- **Make**: Extracted brand/manufacturer
- **Current Bid**: Current auction price
- **Adjusted Price (with fees)**: Current bid × 1.5 to account for fees
- **Comparable Price**: Average price from eBay sold listings
- **Profit Margin %**: Percentage profit margin
- **Profit Amount**: Absolute profit in £
- **Highlight**: "YES" for items meeting profit criteria, "NO" otherwise
- **Auction End Time**: When the auction ends
- **Scraped At**: Timestamp when data was collected

## Configuration

You can customize the behavior by editing variables at the top of `auction_search_app_nobosch.py`:

- `SEARCH_TERMS`: List of brands/manufacturers to search for
- `MAX_PAGES`: Maximum pages to scrape per search term
- `FEE_MULTIPLIER`: Multiplier for auction fees (default: 1.5)
- `MIN_PROFIT_MARGIN`: Minimum profit margin threshold (default: 0.5 = 50%)
- `MIN_PROFIT_AMOUNT`: Minimum profit amount threshold (default: £50)
- `HEADLESS`: Run browser in headless mode (default: True)

## Profit Criteria

Items are highlighted as profitable if they meet **either** of these conditions (not necessarily the higher):
- Profit margin ≥ 50% 
- Profit amount ≥ £50

The adjusted price (current bid × 1.5) is used to account for auction fees, buyer's premium, and other costs.

## Logs

Detailed logs are saved to `auction_results/scrape.log` and also displayed in the console during execution.

## Notes

- The script uses Selenium for auction scraping and requests/BeautifulSoup for eBay price lookups
- Rate limiting and random delays are implemented to avoid overwhelming the servers
- Chrome WebDriver is automatically downloaded and managed via webdriver-manager
- The script handles cookie consent banners automatically

## Troubleshooting

If you encounter issues:
1. Ensure Chrome browser is installed
2. Check your internet connection
3. Review logs in `auction_results/scrape.log`
4. Try reducing `MAX_PAGES` if timeouts occur
5. Set `HEADLESS = False` to see the browser in action for debugging

## License

This tool is for educational and personal use only. Please respect the terms of service of John Pye Auctions and eBay.
