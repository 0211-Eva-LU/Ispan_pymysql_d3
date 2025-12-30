from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime 

# 設定 Chrome 瀏覽器的選項
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗
options.add_argument("--incognito") # 無痕模式
options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。

def pc_home_products(product_name):
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://24h.pchome.com.tw/search/?q={product_name}")

    all_products = []
    while True:
        time.sleep(2)
        info_cards = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2--gridCard")
        print(f"有 {len(info_cards)} 個商品資訊")
        
        page_products = []

        for card in info_cards:
            img_url = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__img img").get_attribute("src")
            link = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__link").get_attribute("href")
            title = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__title").text
            price = card.find_element(By.CSS_SELECTOR, ".c-prodInfoV2__priceValue").text

            if img_url.endswith('.svg'):
                continue

            page_products.append({
                "img_url": img_url,
                "link": link,
                "title": title,
                "price": price,
                "keyword":product_name,
                "scrap_time" : datetime.now(),
            })

        all_products.extend(page_products)
        disabled_btn = driver.find_elements(By.CSS_SELECTOR, ".c-pagination__button.is-next button[disabled]")
        if disabled_btn != []:
            print("已經是最後一頁，無法點擊下一頁按鈕")
            driver.quit()
            break

        next_page_btn = driver.find_element(By.CSS_SELECTOR, ".c-pagination__button.is-next button")
        next_page_btn.click()
    
    with open(f"pc_home_{product_name}.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)