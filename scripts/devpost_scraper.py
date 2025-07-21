import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Define the four sections and their URLs
SECTION_URLS = {
    "staff_picks": "https://devpost.com/software/search?query=is%3Afeatured",
    "popular": "https://devpost.com/software/popular",
    "google_chrome_ai_challenge": "https://devpost.com/software/search?order_by=trending&query=at%3A%22Google+Chrome+Built-in+AI+Challenge%22",
    "built_with_flutter": "https://devpost.com/software/built-with/flutter?order_by=trending",
}

def scrape_section_projects(section_name, base_url, max_pages=3):
    print(f"\n🔍 Scraping section: {section_name}")
    all_projects = []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    for page in range(1, max_pages + 1):
        url = f"{base_url}&page={page}" if "?" in base_url else f"{base_url}?page={page}"
        print(f"  → Scraping {url}")
        driver.get(url)

        # Scroll to bottom to trigger lazy loading
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(1.2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.link-to-software"))
            )
        except:
            print(f"    ❌ Timeout on page {page}")
            continue

        cards = driver.find_elements(By.CSS_SELECTOR, "a.link-to-software")
        print(f"    ✅ Found {len(cards)} projects")

        for card in cards:
            title = card.get_attribute("innerText").strip().split("\n")[0]
            href = card.get_attribute("href")
            all_projects.append({
                "section": section_name,
                "title": title,
                "url": href
            })

    driver.quit()
    return all_projects

# Aggregate results from all sections
all_data = []
for section, url in SECTION_URLS.items():
    all_data.extend(scrape_section_projects(section, url, max_pages=3))

# Save to CSV
df = pd.DataFrame(all_data)
os.makedirs("data", exist_ok=True)
df.to_csv("data/devpost_projects.csv", index=False)

#import ace_tools as tools; tools.display_dataframe_to_user(name="Devpost Projects", dataframe=df)
