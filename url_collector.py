from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://leetcode.com/problemset/")
print(driver.title)
time.sleep(5)


try:
    role_divs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="row"]'))
    )

    urls = []
    for div in role_divs:
        try:
            link = div.find_element(By.CSS_SELECTOR, 'div.truncate a')
            url = link.get_attribute("href")
            if url:
                urls.append(url)
        except:
            print("Link bulunamadı.")

    with open("urls.txt","w") as file:
        for url in urls:
            file.write(url + "\n")
        
    
finally:
    time.sleep(3)
    driver.quit()
