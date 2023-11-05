from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
Titles,descriptions,imageurls,ratings,durations,categories,authors,textbooks,prices=[],[],[],[],[],[],[],[],[]

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('E:/chromedriver_win32/chromedriver.exe', options=options)
url='https://unica.vn/'
driver.get(url)

try:
    cookies_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='webpush-slidedown-allow-button align-right primary slidedown-button']")))
    cookies_button.click()
except:
    pass

nav_list = driver.find_elements(By.XPATH, "//ul[@class='menu']/li/a")
time.sleep(2)
with open('course_urls.txt', 'w') as file:
    for i in range(len(nav_list)):
        time.sleep(3)
        try:
            cookies_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='webpush-slidedown-allow-button align-right primary slidedown-button']")))
            cookies_button.click()
        except:
            pass
        nav_list = driver.find_elements(By.XPATH,"//ul[@class='menu']/li/a")
        category = nav_list[i].text
        hover = ActionChains(driver).move_to_element(nav_list[i])
        hover.perform()
        dropdown = driver.find_element(By.XPATH,f"//ul[@class='menu']/li[{i+1}]/div/div/ul")
        first_dropdown_link = dropdown.find_element(By.XPATH,"./li[1]/a")
        first_dropdown_link.click()
        time.sleep(3)

        last_page_number = int(driver.find_element(By.XPATH, "//ul[contains(@class,'pagination')]/li[last()-1]/a").text)
        course_urls = []
        for page in range(1, last_page_number+1):
            courses = driver.find_elements(By.XPATH, "//a[@class='link-course']")
            for course in courses:
                course_url = course.get_attribute("href")
                file.write(f"{category},{course_url}\n")  
                course_urls.append(course_url)
            for course_url in course_urls:
                driver.get(course_url)
                
                time.sleep(5)
                driver.back()
                time.sleep(5)

            if page != last_page_number:
                new_page = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//li[@class='next']//a")))
                driver.execute_script("arguments[0].scrollIntoView(true);", new_page)
                driver.execute_script("arguments[0].click();", new_page)

        driver.get(url)
        time.sleep(3)
driver.quit()








