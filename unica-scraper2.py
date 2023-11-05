import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('E:/chromedriver_win32/chromedriver.exe', options=options)


with open('course_urls.txt', 'r') as f:
    courses = f.readlines()[:50]

    course_data = []
    for course in courses:
        driver.get(course)
        time.sleep(5)  
        breadcrumb=driver.find_element(By.XPATH,"//div[@class='breadcumb-detail-course']")
        category = driver.find_element(By.XPATH, "//div[contains(@class,'breadcumb-detail-course')]/a[2]")
        course_title = driver.find_element(By.XPATH, '//h1[@itemprop="itemReviewed"]')
        instructor = driver.find_element(By.XPATH, '//div[@class="u-detail-tea"]/a/span')
        element = driver.find_element(By.CSS_SELECTOR,".u-detail-students span")
        students = driver.execute_script("return arguments[0].textContent.trim();", element)
        total_rating = driver.find_element(By.CSS_SELECTOR,"div.u-detail-rate")
        short_intro = driver.find_element(By.XPATH, '//div[@class="u-detail-desc"]')
        long_intro = driver.find_element(By.CSS_SELECTOR, '.u-des-course')
        price = driver.execute_script("return document.querySelector('.big-price').textContent")
        whatlearn=driver.find_element(By.XPATH,"//div[@class='u-learn-what']")
        
        iframe=driver.find_element(By.XPATH,"//iframe[@class='embed-responsive-item img-responsive']")
        duration = driver.find_element(By.XPATH, "//div[@id='sidebar']//li[1]//p")
        coursestruct=driver.find_elements(By.XPATH,"//div[@class='u-list-course']//h2[@class='panel-title']")
        stucomments=driver.find_element(By.XPATH,"//div[@class='u-cm-hv']")
        star_rating = driver.find_element(By.XPATH, "//div[@class='number-big-rate']")
        lectures=driver.find_element(By.XPATH,"//div[@id='sidebar']//li[2]//p")
        instructor_image_url = driver.find_element(By.XPATH, "//div[@class='uct-ava-gv']/img").get_attribute('src')
        print(instructor_image_url)
        instructors_info=driver.find_element(By.XPATH,"//div[@class='uct-right']")
        instructors_courses=driver.find_element(By.XPATH,"//div[@class='uct-rate-gv']/ul/li[2]/span")
        instructors_students=driver.find_element(By.XPATH,"//div[@class='uct-rate-gv']/ul/li[1]/span")
        
        try:
            pub_price=driver.execute_script("return document.querySelector('.small-price2').textContent")
            iframe = driver.find_element(By.XPATH, "//iframe[@class='embed-responsive-item img-responsive']")
            driver.switch_to.frame(iframe)
            canonical_link = driver.find_element(By.XPATH, "//head/link[@rel='canonical']")
            youtube_url = canonical_link.get_attribute('href')
            print(youtube_url)
            thumbnail_div = driver.find_element(By.XPATH, "//div[@class='ytp-cued-thumbnail-overlay-image']")
            thumbnail_image_url = thumbnail_div.get_attribute('style').split('"')[1]
            print(thumbnail_image_url)
            driver.switch_to.parent_frame()
        except :
            pub_price=price
            print("No iframe element found")
            youtube_url = 'None'
            thumbnail_image_url='None'
            driver.switch_to.parent_frame()


        
        course_data.append({
            'Category': category.text,
            'URL': course,
            'Breadcrumb' : breadcrumb.text,
            'Course Title': course_title.text,
            'Instructor': instructor.text,
            'Students': students,
            'Youtube URL': youtube_url,
            'Total Rating': total_rating.text,
            'Short Intro': short_intro.text,
            'Long Intro': long_intro.text,
            'What will you learn':whatlearn.text,
            'Price': price,
            'Publish Price':pub_price,
            'Duration': duration.text,
            'Lectures': lectures.text,
            'Rating': star_rating.text,
            'Instructor Info': instructors_info.text,
            'Instructor Image URL': instructor_image_url,
            'Instructors Courses': instructors_courses.text,
            'Instructors Students': instructors_students.text,
            'Students Comments':stucomments.text,
            'Thumbnail image url':thumbnail_image_url,
            'Course exercises':'',
            'Course materials':'',
            'Date of first publication':'',
            'Date of latest update':''
        })

driver.quit()

df = pd.DataFrame(course_data)
df.to_csv('unica_courses.csv', index=False, encoding='utf-8-sig')

