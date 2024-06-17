from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#変数定義
job_href_list=[]
detail_list=[]
url="https://jp.indeed.com/jobs?q=%E4%BB%8B%E8%AD%B7%E8%81%B7&l=%E6%84%9B%E7%9F%A5%E7%9C%8C&from=searchOnHP&vjk=c6c1a8ac634a101f&advn=193295575071139"

#求人詳細取得定義
def get_detail():
    job_title=driver.find_element(By.TAG_NAME,"h1").text
    company_name=driver.find_element(By.XPATH,"//div[contains(text(), '企業名')]/following-sibling::div[1]").text
    address=driver.find_element(By.XPATH,"//div[contains(text(), '所在地')]/following-sibling::div[1]").text
    point=driver.find_element(By.CSS_SELECTOR,"div>ul").text
    point=point.replace("\n"," ")
    try:
        workhours=driver.find_element(By.CSS_SELECTOR,"div[data-segment-label='WorkHours']").text
        workhours=workhours.replace("\n"," ")
    except:
        workhours=driver.find_element(By.XPATH,"//div[contains(text(), '勤務時間')]/following-sibling::div[1]/p").text
    salary=driver.find_element(By.XPATH,"//*[@id='salaryInfoAndJobType']/span[contains(text(), '円')]").text
    if i==1:
        style="正社員"
    else:
        style="アルバイト"
        
    detail_dict={"題名（介護職）":job_title,"会社名":company_name,"住所":address,"雇用形態":style,"ポイント":point,"勤務時間":workhours,"給料":salary}
    detail_list.append(detail_dict)

#トップページ表示
driver.get(url)
time.sleep(3)

#正社員絞り込み
driver.find_element(By.CSS_SELECTOR,"button[aria-label=雇用形態のフィルター]").click()
time.sleep(1)
driver.find_element(By.XPATH,"//li/a[contains(text(), '正社員')]").click()
time.sleep(3)

#各求人情報ページ取得
while True:
    #ポップアップクローズ
    try:
        driver.find_element(By.CSS_SELECTOR,"button[aria-label='閉じる']").click()
    except:
        pass

    #スクロールダウン
    for i in range(8):
        driver.execute_script('window.scrollBy(0, 1000);')
        time.sleep(1)

    try:
        #次のページがある場合
        next_page=driver.find_element(By.CSS_SELECTOR,"a[aria-label='Next Page']")
        #現在のページの求人ページ取得
        a_tags=driver.find_elements(By.CSS_SELECTOR,"h2>a")

        for a_tag in a_tags:
            job_href=a_tag.get_attribute("href")
            job_href_list.append(job_href)

        print(len(job_href_list))
        next_page.click()
        time.sleep(3)

    except:
        #次のページがない場合
        a_tags=driver.find_elements(By.CSS_SELECTOR,"h2>a")

        for a_tag in a_tags:
            job_href=a_tag.get_attribute("href")
            job_href_list.append(job_href)

        break

#各求人情報ページアクセス、詳細取得
for job_page in job_href_list:
    driver.get(job_page)
    time.sleep(3)
    i=1
    get_detail()

driver.quit()