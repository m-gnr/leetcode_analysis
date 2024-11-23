from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import csv


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
lst = []

def get_element_text(xpath, wait_time=10):
    for _ in range(3):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text
        except StaleElementReferenceException:
            continue  
        except Exception:
            return ""  
    return "" 

with open('links.txt', 'r') as file:
    links = [link.strip() for link in file.readlines()]

try:
    for link in links:
        driver.get(link)
        # time.sleep(2) 

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Subscribe to unlock.')]"))
            )
            continue
        except Exception:
            pass  


        title = get_element_text("(//a[contains(@class, 'no-underline')])[2]")
        difficulty_level = get_element_text("(//div[contains(@class, 'bg-fill-secondary')])[1]")
        submission = get_element_text("//div[text()='Submissions']/following-sibling::div[contains(@class, 'text-label-1')]")
        accepted = get_element_text("//div[text()='Accepted']/following-sibling::div[contains(@class, 'text-label-1')]")
        accepted_rate = get_element_text("//div[text()='Acceptance Rate']/following-sibling::div[contains(@class, 'text-label-1')]")

        try:
            topics_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[.='Topics']/following-sibling::div//a[contains(@class, 'no-underline')]"))
            )
            topics_list = [(element.text, element.get_attribute("href")) for element in topics_elements]
            tags = [url.split('/')[-2] for _, url in topics_list]
        except Exception:
            tags = [""]

        try:
            stats = driver.find_elements(By.XPATH, '//button[contains(@class, "relative")]/div[@class=""]')
            likes = stats[0].text if len(stats) > 0 else '0'
            comments = stats[1].text if len(stats) > 1 else '0'
        except Exception:
            likes = ""
            comments = ""

        lst.append((title, difficulty_level, submission, accepted, accepted_rate, likes, comments, ", ".join(tags)))

finally:

    with open('leetcode_scrap.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Difficulty Level", "Submissions", "Accepted", "Acceptance Rate", "Likes", "Comments", "Tags"])
        writer.writerows(lst)

    driver.quit()

    