import os
import pandas as pd
import time
import re
import requests
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def extract_meta_description(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, "meta[property='og:description']").get_attribute("content").strip()
    except:
        return ""


def extract_section_by_heading(driver, heading_text):
    try:
        element = driver.find_element(By.XPATH, f"//*[text()='{heading_text}']")
        sibling = element.find_element(By.XPATH, "following-sibling::*[1]")
        return sibling.text.strip()
    except:
        return ""


def extract_built_with(driver):
    try:
        heading = driver.find_element(By.XPATH, "//*[text()='Built With']")
        container = heading.find_element(By.XPATH, "following-sibling::*[1]")
        tags = container.find_elements(By.TAG_NAME, "span")
        return ", ".join([tag.text.strip() for tag in tags if tag.text.strip()])
    except:
        return ""


def extract_submitted_to(driver):
    try:
        section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "submissions"))
        )
        return section.find_element(By.CSS_SELECTOR, "div.software-list-content p a").text.strip()
    except Exception as e:
        print(f"❌ Failed to extract 'submitted_to': {e}")
        return ""


def extract_hackathon_url(driver):
    try:
        section = driver.find_element(By.CSS_SELECTOR, "div#submissions.section")
        link = section.find_element(By.TAG_NAME, "a")
        return link.get_attribute("href")
    except Exception:
        return ""


def extract_host_institution_from_hackathon(hackathon_url):
    try:
        response = requests.get(hackathon_url, timeout=10)
        html = response.text
        match = re.search(
            r'<i class="fas fa-map-marker-alt"[^>]*></i>\s*<div class="info">\s*<a [^>]*>([^<]+)</a>',
            html,
            re.IGNORECASE
        )
        if match:
            return match.group(1).strip()
        return ""
    except Exception as e:
        print(f"⚠️ Error fetching host institution from {hackathon_url}: {e}")
        return ""


def extract_project_date(driver):
    try:
        updates_tab = driver.find_elements(By.XPATH, '//a[contains(text(), "Updates")]')
        if updates_tab:
            updates_tab[0].click()
            time.sleep(2)
            time_tags = driver.find_elements(By.CSS_SELECTOR, "time")
            if time_tags:
                raw_date = time_tags[0].get_attribute("datetime").strip()
                return format_project_date(raw_date)
    except Exception as e:
        print(f"⚠️ Failed to extract project date: {e}")
        return ""


def format_project_date(raw_date):
    try:
        dt = datetime.fromisoformat(raw_date.replace("Z", ""))
        return dt.strftime("%m/%d/%Y")
    except Exception as e:
        print(f"⚠️ Error parsing date: {raw_date} → {e}")
        return ""


# Prepare
os.makedirs("screenshots", exist_ok=True)
df = pd.read_csv("data/devpost_projects.csv")
output_path = "data/devpost_projects_enriched.csv"

if os.path.exists(output_path):
    enriched_df = pd.read_csv(output_path)
    enriched_urls = set(enriched_df["url"].dropna())
    print(f"🔄 Resuming... {len(enriched_urls)} already enriched.")
else:
    enriched_df = pd.DataFrame()
    enriched_urls = set()
    print("🔄 Starting fresh enrichment...")

to_enrich = df[~df["url"].isin(enriched_urls)]
print(f"➡️ Enriching {len(to_enrich)} remaining projects.")

driver = create_driver()
new_data = []

for idx, row in tqdm(to_enrich.iterrows(), total=len(to_enrich), desc="Enriching projects"):
    url = row.get("url", "")
    title = str(row.get("title", "")).strip()

    if not isinstance(url, str) or not url.startswith("http"):
        print(f"⚠️ Skipping invalid URL: {url}")
        continue

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        hackathon_url = extract_hackathon_url(driver)

        enriched_row = {
            "title": title,
            "url": url,
            "short_description": extract_meta_description(driver),
            "submitted_to": extract_submitted_to(driver),
            "built_with": extract_built_with(driver),
            "inspiration": extract_section_by_heading(driver, "Inspiration"),
            "what_it_does": extract_section_by_heading(driver, "What it does"),
            "how_we_built_it": extract_section_by_heading(driver, "How we built it"),
            "host_institution": extract_host_institution_from_hackathon(hackathon_url),
            "project_date": extract_project_date(driver)
        }

        new_data.append(enriched_row)

    except (InvalidSessionIdException, WebDriverException) as e:
        print(f"❌ Browser session failed, restarting: {e}")
        try:
            driver.quit()
        except:
            pass
        driver = create_driver()
        continue

    except Exception as e:
        print(f"⚠️ Error enriching {url}: {e}")
        try:
            driver.save_screenshot(f"screenshots/fail_enrich_{idx}.png")
        except:
            print("⚠️ Could not take screenshot (session may have ended)")
        continue

driver.quit()

# Save final output
final_df = pd.concat([enriched_df, pd.DataFrame(new_data)], ignore_index=True)
final_df.to_csv(output_path, index=False, na_rep="")
print(f"\n✅ Saved enriched data to {output_path}")
