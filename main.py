import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SAVE_DIR = 'reels'
os.makedirs(SAVE_DIR, exist_ok=True)

def set_chrome_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

# Previous download_video function is modified
# I can't get [ts, _ts, _tsc, _s] tokens, so I changed the method
# Using selenium
def download_video(insta_url, file_name):
    driver = set_chrome_driver()
    driver.get('https://fastdl.app/en')

    wait = WebDriverWait(driver, 15)

    input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-form__input")))
    input_box.clear()
    input_box.send_keys(insta_url)

    download_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.search-form__button')))
    download_btn.click()

    video_link_elem = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.button__download'))
    )
    video_url = video_link_elem.get_attribute('href')
    #print(f"Download link is taken: {video_url}") # For debugging

    res = requests.get(video_url, stream=True)
    res.raise_for_status()
    save_path = os.path.join(SAVE_DIR, file_name)
    with open(save_path, 'wb') as f:
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"{file_name} Download success!")

def main():
    with open('links.txt', 'r') as f:
        content = f.read().strip()
    links = [link.strip() for link in content.split(',') if link.strip()]

    for i, link in enumerate(links, 1):
        file_name = f"Reels{i}.mp4"
        print(f"[{i}/{len(links)}] {link} Download starting...")
        download_video(link, file_name)

if __name__ == "__main__":
    main()

