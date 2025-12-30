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


def momo_products(product_name):
    driver = webdriver.Chrome(options=options)
    # product_name = "ROG滑鼠"
    driver.get(f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={product_name}&_isFuzzy=0&searchType=1")

    all_products = []

    while True:
        time.sleep(2)
        info_cards = driver.find_elements(By.CSS_SELECTOR, ".listAreaLi")
        print(f"有 {len(info_cards)} 個商品資訊")

        for card in info_cards:
            img_url = card.find_element(By.CSS_SELECTOR, "img.goods-img").get_attribute("src")
            link = card.find_element(By.CSS_SELECTOR, "a.prdName").get_attribute("href")
            title = card.find_element(By.CSS_SELECTOR, "a.prdName").text
            price = card.find_element(By.CSS_SELECTOR, "span.price > b").text

            all_products.append({
                "img_url": img_url,
                "link": link,
                "title": title,
                "price": price,
                "keyword":product_name,
                "scrap_time" : datetime.now(),
            })

        next_buttons = driver.find_elements(By.CSS_SELECTOR, "div.page-btn.page-next > a")

        if next_buttons == []:
            print("已經是最後一頁，無法點擊下一頁按鈕")
            break
        
        driver.find_elements(By.CSS_SELECTOR, "div.page-btn.page-next > a")[1].click()
        
    driver.quit()

    with open(f"momo_{product_name}.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)
