# Example Usage and Output Format

## Running the Application

To run the auction scraper:

```bash
python auction_search_app_nobosch.py
```

## Configuration Options

You can customize the behavior by editing these variables in `auction_search_app_nobosch.py`:

```python
# Limit pages to scrape per search term (default: 5)
MAX_PAGES = 5

# Run browser in headless mode (default: True)
HEADLESS = True

# Fee multiplier for auction costs (default: 1.5 = 150%)
FEE_MULTIPLIER = 1.5

# Minimum profit margin to highlight (default: 0.5 = 50%)
MIN_PROFIT_MARGIN = 0.5

# Minimum profit amount to highlight (default: £50)
MIN_PROFIT_AMOUNT = 50.0
```

## Expected Output

### Console Output

```
2026-02-03 10:30:00 - INFO - [BMW] Page 1 (limit 5)
2026-02-03 10:30:05 - INFO - [BMW] Page 1: 20 new links (total 20)
2026-02-03 10:30:10 - INFO - [BMW] Collected 20 unique lot links.
2026-02-03 10:30:15 - INFO - Scraping 20 lot detail pages (term 'BMW').
2026-02-03 10:30:20 - INFO - Found eBay sold price for 'BMW123 BMW': £125.50
2026-02-03 10:35:00 - INFO - Saved 20 rows to auction_results/bosch_lots.csv (sorted by auction end time)
2026-02-03 10:35:00 - INFO - Found 5 items meeting profit criteria (>50% margin OR >£50 profit)
```

### CSV Output Format

The CSV file (`auction_results/bosch_lots.csv`) contains these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Link | Auction listing URL | https://www.johnpyeauctions.co.uk/Event/LotDetails/12345 |
| Title | Full item description | BMW Brake Pad Set 34116775314 |
| Part Number | Extracted part number | 34116775314 |
| Make | Brand/manufacturer | BMW |
| Current Bid | Current auction price | 45.00 |
| Adjusted Price (with fees) | Current bid × 1.5 | 67.50 |
| Comparable Price | Avg eBay sold price | 120.00 |
| Profit Margin % | (Comparable - Adjusted) / Adjusted × 100 | 77.78 |
| Profit Amount | Comparable - Adjusted | 52.50 |
| Highlight | YES if profitable, NO otherwise | YES |
| Auction End Time | When auction ends | 02/05/2026 14:30:00 |
| Scraped At | Timestamp of scrape | 2026-02-03 10:30:45 UTC |

### Example CSV Rows

**Profitable Item (Highlighted):**
```csv
Link,Title,Part Number,Make,Current Bid,Adjusted Price (with fees),Comparable Price,Profit Margin %,Profit Amount,Highlight,Auction End Time,Scraped At
https://www.johnpyeauctions.co.uk/Event/LotDetails/12345,BMW Brake Pad Set 34116775314,34116775314,BMW,45.00,67.50,120.00,77.78,52.50,YES,02/05/2026 14:30:00,2026-02-03 10:30:45 UTC
```

**Non-Profitable Item:**
```csv
Link,Title,Part Number,Make,Current Bid,Adjusted Price (with fees),Comparable Price,Profit Margin %,Profit Amount,Highlight,Auction End Time,Scraped At
https://www.johnpyeauctions.co.uk/Event/LotDetails/67890,NGK Spark Plug LFR5A,LFR5A,NGK,25.00,37.50,42.00,12.00,4.50,NO,02/05/2026 15:00:00,2026-02-03 10:31:15 UTC
```

## Interpreting Results

### Highlight Column
- **YES**: Item meets profit criteria (≥50% margin OR ≥£50 profit)
- **NO**: Item does not meet profit criteria

### Key Metrics to Watch

1. **Profit Margin %**: Higher is better. Look for items with 50%+ margins
2. **Profit Amount**: Absolute profit after fees. Look for £50+ items
3. **Auction End Time**: Items are sorted by this (soonest first), so check the top rows for urgent opportunities

### Tips for Finding Good Deals

1. Focus on items marked **Highlight: YES** at the top of the CSV
2. Cross-check the comparable price with recent eBay sales
3. Consider the auction end time - items ending soon may have less competition
4. Review the part number and title to ensure it matches what you're looking for
5. Factor in your own shipping and handling costs

## Log Files

Detailed logs are saved to `auction_results/scrape.log` for troubleshooting.
