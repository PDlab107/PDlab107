import csv
import os
import re
import time
import logging
import random
from datetime import datetime
from urllib.parse import urljoin

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
SCROLL_PAUSE = 0.3
DEBUG_SAVE_HTML = False
SLEEP_BETWEEN_LOTS = (0.7, 1.4)
SLEEP_BETWEEN_PAGES = (1.0, 1.8)

FIELDNAMES = ["Link", "Title", "Time Remaining", "Current Bid", "Scraped At"]

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
    Uses exponential backoff for retries.
    """
    for attempt in range(3):
        try:
            element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            if attempt < 2:  # Don't sleep on the last attempt
                wait_time = 0.5 * (2 ** attempt)  # Exponential backoff: 0.5s, 1s
                logging.warning(f"Attempt {attempt + 1} failed for {locator}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logging.warning(f"Attempt {attempt + 1} failed for {locator}.")
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

        # Scroll to bottom once to load dynamic content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        # Scroll back to top to ensure all elements are accessible
        driver.execute_script("window.scrollTo(0, 0);")
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
    # Combined pattern to search for multiple conditions in one XPath query
    combined_pattern = (
        "//*[(contains(@id,'bid') or contains(@class,'bid') or "
        "contains(@class,'price') or contains(text(),'Current Bid') or "
        "contains(text(),'current bid')) and contains(text(),'£')]"
    )
    try:
        nodes = driver.find_elements(By.XPATH, combined_pattern)
        for n in nodes:
            price = extract_price(n.text)
            if price:
                return price
    except Exception:
        pass
    
    # Fallback: search all elements with pound signs
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
    current_bid = extract_current_bid(driver)

    if DEBUG_SAVE_HTML and (not title or not current_bid):
        with open(os.path.join(OUTPUT_DIR, f"debug_lot_{index}.html"), "w", encoding="utf-8") as fh:
            fh.write(driver.page_source)

    if not title:
        logging.warning(f"[{index}] Empty Title: {link}")
    if not current_bid:
        logging.warning(f"[{index}] Empty Current Bid: {link}")

    return {
        "Link": link,
        "Title": title,
        "Time Remaining": time_val,
        "Current Bid": current_bid,
        "Scraped At": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

def scrape_search_term(driver, term, global_seen_links):
    """
    Scrape a single search term using the provided driver instance.
    Returns list of row data for lots not already in global_seen_links.
    """
    rows = []
    try:
        links = collect_lot_links(driver, term)
        if not links:
            logging.warning(f"No links for term '{term}'.")
            return rows

        # Filter out already-scraped links
        new_links = [link for link in links if link not in global_seen_links]
        if len(new_links) < len(links):
            logging.info(f"Skipping {len(links) - len(new_links)} already-scraped lots for term '{term}'.")
        
        if not new_links:
            logging.info(f"All links for term '{term}' already scraped.")
            return rows

        logging.info(f"Scraping {len(new_links)} lot detail pages (term '{term}').")
        for idx, link in enumerate(new_links, start=1):
            rsleep(*SLEEP_BETWEEN_LOTS)
            row = scrape_lot_page(driver, link, idx)
            if row:
                rows.append(row)
                global_seen_links.add(link)
        return rows
    except Exception as e:
        logging.error(f"Error processing term '{term}': {e}")
        return rows

def save_csv(rows):
    if not rows:
        logging.warning("No rows to save.")
        return
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    logging.info(f"Saved {len(rows)} rows to {OUTPUT_FILE}")

def main():
    all_rows = []
    global_seen_links = set()  # Track scraped links across all search terms
    driver = None
    
    try:
        driver = init_driver()
        for term in SEARCH_TERMS:
            term_rows = scrape_search_term(driver, term, global_seen_links)
            all_rows.extend(term_rows)
    finally:
        if driver:
            driver.quit()
    
    save_csv(all_rows)
    print(f"Finished. Unique lots scraped: {len(all_rows)} -> {OUTPUT_FILE}")

if __name__ == "__main__":
    main()