import csv
import os
import re
import time
import logging
import random
from datetime import datetime
from urllib.parse import urljoin, quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

# ---------------- Configuration ----------------
BASE_SEARCH_URL = "https://www.johnpyeauctions.co.uk/Browse?FullTextQuery={query}"
SEARCH_TERMS = [
    "AISIN",
    "Angry Jester",
    "Anschler",
    "Arnott",
    "Ava Cooling",
    "BILSTEIN",
    "BLUEPRINT",
    "BMW",
    "Brembo",
    "Citroen",
    "Corteco",
    "DAYCO",
    "Delphi",
    "Denso",
    "EBC",
    "Eicher",
    "EMPI",
    "FAG",
    "FAI",
    "Febi",
    "H&R",
    "Haldex",
    "Heat Sealer",
    "Hella",
    "Hyundai",
    "INA",
    "Knorr Bremse",
    "Koni",
    "KYB",
    "Laser",
    "Lemforder",
    "LUK",
    "MAGNETI MARELLI",
    "Mahle",
    "MARELLI",
    "Mintex",
    "Mishimoto",
    "Moog",
    "Motormax",
    "NGK",
    "Nissan",
    "Nissens",
    "Pagid",
    "Porsche",
    "Powerflex",
    "Powertec",
    "Quinton Hazell",
    "SACHS",
    "SBS",
    "Sealey",
    "Serbro",
    "SKF",
    "Ssangyong",
    "Starline",
    "Transmech",
    "TYC",
    "VALEO",
    "Vauxhall",
    "VDO",
    "VISTEON",
    "VNE",
    "VW",
    "Wabco",
    "Werkzeug",
    "Yamaha",
    "Zimmerman",
    "Pierburg",
    "VEMO",
    "Mikayo",
    "Gedore",
    "Europa"
]

OUTPUT_DIR = "auction_results"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "bosch_lots.csv")

MAX_PAGES = 5
PAGE_HARD_LIMIT = 5
STOP_IF_NO_NEW_LINKS = True

HEADLESS = True
PAGE_LOAD_TIMEOUT = 25
ELEMENT_WAIT = 12
SCROLL_PAUSE = 1.0
DEBUG_SAVE_HTML = False
SLEEP_BETWEEN_LOTS = (0.7, 1.4)
SLEEP_BETWEEN_PAGES = (1.0, 1.8)

# Fee multiplier to account for auction fees
FEE_MULTIPLIER = 1.5

# Profit thresholds
MIN_PROFIT_MARGIN = 0.5  # 50%
MIN_PROFIT_AMOUNT = 50.0  # £50

FIELDNAMES = [
    "Link", "Title", "Part Number", "Make", "Current Bid", 
    "Adjusted Price (with fees)", "Comparable Price", "Profit Margin %", 
    "Profit Amount", "Highlight", "Auction End Time", "Scraped At"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(OUTPUT_DIR, "scrape.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console)

def rsleep(a, b):
    time.sleep(random.uniform(a, b))

def init_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

def robust_find_element(driver, locator, timeout=12):
    """
    Tries to find an element with retries to handle transient issues more gracefully.
    """
    for attempt in range(3):
        try:
            element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logging.warning(f"Attempt {attempt + 1} failed for {locator}. Retrying...")
            time.sleep(2)
    raise TimeoutException(f"Element {locator} could not be located after retries.")

def accept_cookies(driver):
    try:
        btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(.,'ACCEPT','accept'),'accept')]"))
        )
        btn.click()
        logging.info("Accepted cookies.")
        rsleep(0.4, 0.8)
    except TimeoutException:
        logging.info("Cookie banner not present.")

def collect_lot_links(driver, search_term):
    search_url = BASE_SEARCH_URL.format(query=search_term)
    driver.get(search_url)
    accept_cookies(driver)
    all_links = set()
    page = 1
    prev_total = 0

    while page <= MAX_PAGES and page <= PAGE_HARD_LIMIT:
        logging.info(f"[{search_term}] Page {page} (limit {MAX_PAGES})")

        try:
            robust_find_element(driver, (By.XPATH, "//a[contains(@href,'/Event/LotDetails/')]"), timeout=ELEMENT_WAIT)
        except TimeoutException:
            logging.warning(f"[{search_term}] No lot links found on page {page}, stopping.")
            break

        for _ in range(4):
            driver.execute_script("window.scrollBy(0, 900);")
            time.sleep(SCROLL_PAUSE)

        anchors = driver.find_elements(By.XPATH, "//a[contains(@href,'/Event/LotDetails/')]")
        new_count = 0
        for a in anchors:
            try:
                href = a.get_attribute("href")
                if not href:
                    continue
                if href.startswith("/"):
                    href = urljoin(search_url, href)
                href = href.split("#")[0].strip()
                if "/Event/LotDetails/" in href and href not in all_links:
                    all_links.add(href)
                    new_count += 1
            except StaleElementReferenceException:
                continue

        logging.info(f"[{search_term}] Page {page}: {new_count} new links (total {len(all_links)})")

        if STOP_IF_NO_NEW_LINKS and new_count == 0:
            logging.info("No new links on this page. Assuming end of results.")
            break

        page += 1
        if page > MAX_PAGES or page > PAGE_HARD_LIMIT:
            logging.info("Reached configured page limit. Stopping pagination.")
            break

        advanced = False
        next_selectors = [
            "//a[contains(@aria-label,'Next') and not(contains(@class,'disabled'))]",
            "//a[contains(text(),'Next') and not(contains(@class,'disabled'))]",
            "//a[contains(text(),'»') and not(contains(@class,'disabled'))]",
            "//button[contains(text(),'Next') and not(@disabled)]"
        ]
        for sel in next_selectors:
            try:
                nxt = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, sel)))
                cls = (nxt.get_attribute("class") or "").lower()
                if "disabled" in cls:
                    continue
                nxt.click()
                advanced = True
                rsleep(*SLEEP_BETWEEN_PAGES)
                break
            except TimeoutException:
                continue
            except Exception:
                continue

        if not advanced:
            logging.info("No active next-page control; stopping pagination.")
            break

        if prev_total == len(all_links):
            logging.info("Total links unchanged after page advance; stopping to prevent loop.")
            break
        prev_total = len(all_links)

    logging.info(f"[{search_term}] Collected {len(all_links)} unique lot links.")
    return list(all_links)

def extract_price(text):
    if not text:
        return ""
    m = re.search(r"£\s*([\d,]+(?:\.\d{1,2})?)", text)
    if not m:
        return ""
    num = m.group(1).replace(",", "")
    if "." not in num:
        num += ".00"
    elif len(num.split(".")[1]) == 1:
        num += "0"
    return num

def extract_current_bid(driver):
    patterns = [
        "//*[contains(@id,'bid') and contains(text(),'£')]",
        "//*[contains(@class,'bid') and contains(text(),'£')]",
        "//*[contains(@class,'price') and contains(text(),'£')]",
        "//*[contains(text(),'Current Bid') or contains(text(),'current bid')]",
    ]
    for xp in patterns:
        try:
            nodes = driver.find_elements(By.XPATH, xp)
            for n in nodes:
                price = extract_price(n.text)
                if price:
                    return price
        except Exception:
            continue
    try:
        pound_nodes = driver.find_elements(By.XPATH, "//*[contains(text(),'£')]")
        for el in pound_nodes:
            price = extract_price(el.text)
            if price:
                return price
    except Exception:
        pass
    return ""

def parse_time_string(raw):
    if not raw:
        return ""
    raw = raw.strip()
    if re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", raw):
        return raw
    iso = re.match(r"(\d{4})-(\d{2})-(\d{2})[T\s](\d{2}):(\d{2}):(\d{2})", raw)
    if iso:
        y, m, d, H, M, S = iso.groups()
        return f"{m}/{d}/{y} {H}:{M}:{S}"
    if raw.isdigit() and len(raw) >= 10:
        try:
            dt = datetime.utcfromtimestamp(int(raw))
            return dt.strftime("%m/%d/%Y %H:%M:%S")
        except:
            pass
    slash = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", raw)
    if slash:
        p1, p2, y = slash.groups()
        m, d = p1, p2
        if int(p1) > 12 and int(p2) <= 12:
            m, d = p2, p1
        return f"{int(m):02d}/{int(d):02d}/{y} 00:00:00"
    return raw

def find_data_attr(driver, attrs):
    for attr in attrs:
        try:
            el = driver.find_element(By.XPATH, f"//*[@{attr}]")
            val = el.get_attribute(attr)
            if val:
                return val.strip()
        except NoSuchElementException:
            continue
    return ""

def extract_title(driver):
    try:
        h3 = driver.find_element(By.XPATH, "//h3[contains(@class, 'detail__title')]")
        title = h3.get_attribute("innerText").strip()
        title = re.sub(r"\s+", " ", title)
        return title
    except Exception as e:
        logging.warning(f"Failed to extract title: {e}")
        return ""

def extract_part_number(title):
    """
    Extract part number from title.
    Common patterns: alphanumeric codes, numbers with hyphens/slashes
    """
    if not title:
        return ""
    
    # Pattern 1: Common part number formats (e.g., 12345-678, ABC123, 123.456.789)
    patterns = [
        r'\b([A-Z0-9]{3,}[-./][A-Z0-9]+(?:[-./][A-Z0-9]+)*)\b',  # ABC-123-456
        r'\b([0-9]{5,})\b',  # 5+ digit numbers
        r'\b([A-Z]{2,}[0-9]{3,}[A-Z0-9]*)\b',  # AB12345
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return ""

def extract_make(title):
    """
    Extract manufacturer/brand from title using the search terms list
    """
    if not title:
        return ""
    
    title_upper = title.upper()
    for term in SEARCH_TERMS:
        if term.upper() in title_upper:
            return term
    
    # Try to find brand at start of title
    words = title.split()
    if words and len(words[0]) > 2:
        return words[0]
    
    return ""

def get_ebay_sold_price(part_number, make, title):
    """
    Search eBay sold listings to get comparable price
    Uses requests + BeautifulSoup for lightweight scraping
    """
    if not part_number and not make:
        logging.warning(f"No part number or make to search: {title[:50]}")
        return None
    
    # Build search query
    search_terms = []
    if part_number:
        search_terms.append(part_number)
    if make:
        search_terms.append(make)
    
    query = " ".join(search_terms)
    
    # eBay sold listings URL
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={quote_plus(query)}&LH_Sold=1&LH_Complete=1&_sop=13"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find sold prices
        prices = []
        
        # Look for price elements in search results
        price_elements = soup.find_all('span', class_='s-item__price')
        for elem in price_elements[:10]:  # Check first 10 results
            price_text = elem.get_text()
            price = extract_price(price_text)
            if price:
                try:
                    prices.append(float(price))
                except ValueError:
                    continue
        
        if prices:
            # Return average of top 5 sold prices
            avg_price = sum(prices[:5]) / min(len(prices), 5)
            logging.info(f"Found eBay sold price for '{query}': £{avg_price:.2f}")
            return round(avg_price, 2)
        else:
            logging.warning(f"No sold prices found for '{query}'")
            return None
            
    except Exception as e:
        logging.warning(f"Error fetching eBay prices for '{query}': {e}")
        return None

def scrape_lot_page(driver, link, index):
    try:
        driver.get(link)
    except Exception as e:
        logging.error(f"[{index}] Failed load {link}: {e}")
        return None

    try:
        WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except TimeoutException:
        logging.error(f"[{index}] Body timeout {link}")
        return None

    title = extract_title(driver)

    time_val = find_data_attr(driver, ["data-action-time", "data-countdown", "data-endtime", "data-end-time"])
    if not time_val:
        body = driver.find_element(By.TAG_NAME, "body").text
        dt = re.search(r"\b\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}\b", body)
        if dt:
            time_val = dt.group(0)
        else:
            iso = re.search(r"\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}\b", body)
            if iso:
                time_val = iso.group(0)

    time_val = parse_time_string(time_val)
    current_bid_str = extract_current_bid(driver)

    if DEBUG_SAVE_HTML and (not title or not current_bid_str):
        with open(os.path.join(OUTPUT_DIR, f"debug_lot_{index}.html"), "w", encoding="utf-8") as fh:
            fh.write(driver.page_source)

    if not title:
        logging.warning(f"[{index}] Empty Title: {link}")
    if not current_bid_str:
        logging.warning(f"[{index}] Empty Current Bid: {link}")

    # Extract part number and make
    part_number = extract_part_number(title)
    make = extract_make(title)
    
    # Calculate adjusted price with fees
    current_bid = 0.0
    adjusted_price = 0.0
    if current_bid_str:
        try:
            current_bid = float(current_bid_str)
            adjusted_price = current_bid * FEE_MULTIPLIER
        except ValueError:
            logging.warning(f"[{index}] Could not convert bid to float: {current_bid_str}")
    
    # Get comparable price from eBay
    comparable_price = get_ebay_sold_price(part_number, make, title)
    
    # Calculate profit metrics
    profit_margin = 0.0
    profit_amount = 0.0
    highlight = "NO"
    
    if comparable_price and adjusted_price > 0:
        profit_amount = comparable_price - adjusted_price
        profit_margin = (profit_amount / adjusted_price) * 100 if adjusted_price > 0 else 0
        
        # Determine if item should be highlighted
        if profit_margin >= (MIN_PROFIT_MARGIN * 100) or profit_amount >= MIN_PROFIT_AMOUNT:
            highlight = "YES"
    
    return {
        "Link": link,
        "Title": title,
        "Part Number": part_number,
        "Make": make,
        "Current Bid": f"{current_bid:.2f}" if current_bid > 0 else "",
        "Adjusted Price (with fees)": f"{adjusted_price:.2f}" if adjusted_price > 0 else "",
        "Comparable Price": f"{comparable_price:.2f}" if comparable_price else "",
        "Profit Margin %": f"{profit_margin:.2f}" if comparable_price else "",
        "Profit Amount": f"{profit_amount:.2f}" if comparable_price else "",
        "Highlight": highlight,
        "Auction End Time": time_val,
        "Scraped At": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

def scrape_search_term(term):
    driver = init_driver()
    rows = []
    try:
        links = collect_lot_links(driver, term)
        if not links:
            logging.warning(f"No links for term '{term}'.")
            return rows

        logging.info(f"Scraping {len(links)} lot detail pages (term '{term}').")
        for idx, link in enumerate(links, start=1):
            rsleep(*SLEEP_BETWEEN_LOTS)
            row = scrape_lot_page(driver, link, idx)
            if row:
                rows.append(row)
        return rows
    finally:
        driver.quit()

def parse_auction_end_time(time_str):
    """
    Parse auction end time string to datetime for sorting
    """
    if not time_str:
        return datetime.max  # Put items without time at end
    
    try:
        # Try MM/DD/YYYY HH:MM:SS format
        if re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", time_str):
            return datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
        # Try other formats
        return datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
    except:
        return datetime.max

def save_csv(rows):
    if not rows:
        logging.warning("No rows to save.")
        return
    
    # Sort by auction end time (soonest first)
    sorted_rows = sorted(rows, key=lambda x: parse_auction_end_time(x.get("Auction End Time", "")))
    
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in sorted_rows:
            writer.writerow(r)
    logging.info(f"Saved {len(sorted_rows)} rows to {OUTPUT_FILE} (sorted by auction end time)")
    
    # Print summary of highlighted items
    highlighted = [r for r in sorted_rows if r.get("Highlight") == "YES"]
    logging.info(f"Found {len(highlighted)} items meeting profit criteria (>50% margin OR >£50 profit)")

def main():
    all_rows = []
    for term in SEARCH_TERMS:
        term_rows = scrape_search_term(term)
        all_rows.extend(term_rows)
    save_csv(all_rows)
    print(f"Finished. Rows: {len(all_rows)} -> {OUTPUT_FILE}")

if __name__ == "__main__":
    main()