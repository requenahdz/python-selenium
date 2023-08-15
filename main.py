from pickle import TRUE
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json
import pyautogui
import time
import pygetwindow

service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
now = datetime.datetime.now()

try:
    driver.get("http://localhost:3000")
    driver.implicitly_wait(10)  

    with open('CUSTOMER.json', 'r') as archivo_json:
        datos = json.load(archivo_json)
        for item in datos:
            try:
                driver.execute_script("window.scrollBy(0, {});".format(50))
                time.sleep(1)
                if "type" not in item:
                    item['type'] = "input"

                if "emailTest" in item and item["emailTest"]==True:
                     item['value'] = "test"+str(now.hour).zfill(2)+str(now.minute).zfill(2)+"@robertorequena.mx"
                
                
                if  item["type"] == 'input':
                    if  "xpat" in item:
                        element = driver.find_element(By.XPATH,item["xpat"])
                        element.click()
                        element.send_keys(item['value'])
                        
                    if  "name" in item:
                        element = driver.find_element(By.NAME,item["name"])
                        element.click()
                        element.send_keys(item['value']) 
                    
                if  item["type"] == 'button':
                    wait = WebDriverWait(driver, 10)  # Esperar hasta 10 segundos
                    if  "selector" in item:
                        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, item["selector"])))
                    if "xpat" in item:
                        element = wait.until(EC.presence_of_element_located((By.XPATH, item["xpat"])))
                    element.click()
                    
                if  item["type"] == 'file':
                    element = driver.find_element(By.CSS_SELECTOR,item["selector"])
                    element.click()
                    
                    #windows = pygetwindow.getWindowsWithTitle("Finder")
            
        
                
                print("LISTO: "+item["name"]+" "+item["value"])
            except Exception as e:
                print(e)
         
finally:
    print("Fin")
    #driver.quit()
