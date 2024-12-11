from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import pandas as pd

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.myntra.com")

search_bar = driver.find_element(By.CLASS_NAME, "desktop-searchBar")

search_bar.send_keys("sweatshirt for women")
search_bar.send_keys(Keys.RETURN)

time.sleep(2)
group=[]
Items={}
products = driver.find_elements(By.CLASS_NAME, "product-productMetaInfo")
leng=1
print(len(products),' results found.')
for product in products:
    group.append(product.text)
    

for i in group:
    item=i.split('\n')
    
    Items['Item'+str(leng)]={'product':item[1],'brand':item[0],'price':item[2]}
    leng+=1

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")
links=[]
search_results = soup.find_all("h3")  
leng=1
print(len(search_results),' results found.')
for result in search_results:
    link = "https://www.myntra.com/"+result.find_parent("a")["href"]
    Items['Item'+str(leng)].update({'link':link})
    links.append(link)
    leng+=1
error=''
leng=1
for link in links:
    driver.get(link)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        element=driver.find_element(By.CLASS_NAME, "index-showMoreText")
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
    except Exception as e:
        error=e
    finally:
        itemskey = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "index-rowKey")))
        itemsvalue = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "index-rowValue")))
        
        for i in range(len(itemskey)):
            Items['Item'+str(leng)].update({itemskey[i].text:itemsvalue[i].text})
        leng+=1
        
driver.quit()
with open ('data.txt','w+') as fo:
    json.dump(Items,fo,indent=4,separators=(' ,',' = '))
    print("json done!")

with open ('details.json','w+') as fe:
    
    json.dump(Items,fo,indent=4,separators=(' ,',' = '))
    print("json file done!")