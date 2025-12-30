import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime
# from webdriver_manager.chrome import ChromeDriverManager

# 建立 Service 物件，指定 chromedriver.exe 的路徑


# 設定 Chrome 瀏覽器的選項
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗
options.add_argument("--incognito") # 無痕模式
options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。

# 建立 Chrome 瀏覽器物件
driver = webdriver.Chrome(options=options)
driver.get("https://online.carrefour.com.tw/")
time.sleep(3)

def get_all_product(productname):
    product_info = []
    error_info = []
    wait = WebDriverWait(driver, 10)
    search_but=driver.find_element(By.CSS_SELECTOR,".logo-search.fleft input")
    search_but.clear() 
    search_but.send_keys(productname)
    driver.find_element(By.CSS_SELECTOR,"#search").click()
    
    
    while  True :
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".hot-recommend.clearfix .hot-recommend-item.line")
            )
        )
        time.sleep(4)   
        search_all=driver.find_elements(By.CSS_SELECTOR,".hot-recommend.clearfix .hot-recommend-item.line")
        
        for inedx,product in enumerate(search_all):
            try:
                product_name = product.find_element(By.CSS_SELECTOR,".box-img a").get_attribute("data-name")
                product_price = product.find_element(By.CSS_SELECTOR,".box-img a").get_attribute("data-price")
                product_url = product.find_element(By.CSS_SELECTOR,".box-img a").get_attribute("href")
                product_img = product.find_element(By.CSS_SELECTOR,".box-img .m_lazyload").get_attribute("src")

                if inedx == 0 and productname not in product_name :
                    break


                if productname in product_name :
                    product_info.append({
                        "product_name": product_name,
                        "product_price":product_price.split(".")[0],
                        "product_url":product_url,
                        "product_img": product_img,
                        "scrap_time" : datetime.now(),
                        "keyword":productname
                    })
            except (StaleElementReferenceException, NoSuchElementException) as e:
                    error_info.append({"爬取商品錯誤":str(e)})
                    continue
            
        try:
            next_btn  = driver.find_element(By.CSS_SELECTOR, "img[alt='next']")
            li_elem = next_btn.find_element(By.XPATH, "./ancestor::li[1]")
            li_class=li_elem.get_attribute('class')
        except NoSuchElementException :
            error_info.append({"點選下一頁錯誤":"NoSuchElementException"})
            print('按不到下一頁提前結束')
            break

        if "disabled" in li_class:
            print("已至最後一頁")
            break
        else:
            next_btn.click() 
    
    
    if error_info :
        folder = 'carrefour_products'
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"Carrefour-error-{productname}.json")

        with open(file_path,exit_ok=True) as f :
            json.dump(error_info,f,indent=4,ensure_ascii=False)
        print(f'共{len(error_info)}筆錯誤,已寫入:{file_path}')
    

    if product_info :
        folder = "Carrefour_products"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"{productname}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(product_info, f, indent=4, ensure_ascii=False)

        print(f"共 {len(product_info)} 筆，已寫入：{file_path}")
    else:
        print("沒有搜尋到結果")
    


