from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
import json

class ProfileAssignment:
    def __init__(self):
        options = ChromeOptions()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.stfrancismedicalcenter.com/find-a-provider/")
        WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(By.ID, "MainZone"))
        # yield scrapy.Request("https://www.stfrancismedicalcenter.com/find-a-provider/", callback=self.parse)
        # print("hello")
        # sleep(10)
        res = []
        page=1
        while True:
            try:
                ul = self.driver.find_element(By.XPATH,"//div[@id='PhysicianSearch']/div[2]/ul[1]")
                i = 2
                while True:
                    try:
                        path = ".//li["+str(i)+"]/a[1]"
                        a = ul.find_element(By.XPATH,path)
                        self.driver.execute_script("arguments[0].scrollIntoView()",a)
                        self.driver.execute_script("arguments[0].click()",a)
                        WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(By.ID, "MainZone"))
                        val = self.parse_profile()
                        res.append(val)
                        self.driver.back()
                        ul = WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//div[@id='PhysicianSearch']/div[2]/ul[1]"))
                        i += 1
                    except NoSuchElementException as e1 :
                        break
                a = self.driver.find_element(By.XPATH, "//a[@class='next']")
                if page==40:
                    break
                page+=1
                if not(a.is_enabled()):
                    raise NoSuchElementException
                a.click()
                sleep(2)
            except NoSuchElementException as e:
                self.driver.quit()
                break
        y = {"details":res}
        print(y)
        with open("sample.json", "w") as outfile:
            json.dump(y,outfile)
    def parse_profile(self):
        d = dict()
        ul = self.driver.find_element(By.XPATH,"//article[@id='PhysicianContent']")
        full_name = ul.find_element(By.XPATH,".//h1[1]").text
        ul = ul.find_element(By.XPATH,".//ul[1]")
        try : 
            Speciality = ul.find_element(By.XPATH,"//div[@class='two-thirds']").text or ""
        except NoSuchElementException:
            Speciality=""
        try:
            add_specality = ul.find_element(By.XPATH,".//li[3]")
            temp = add_specality.find_element(By.XPATH,".//strong[1]").text
            if temp.find("Additional") != -1:
                add_specality = add_specality.find_element(By.XPATH,".//span[1]").text
            else:
                add_specality=""
        except NoSuchElementException:
            add_specality=""
        try :
            address = self.driver.find_element(By.XPATH,"//address[1]").text
            temp = address.split(",")
            st=temp[len(temp)-1].split()
            state = st[0]
            zip =st[1]
            temp = temp[len(temp)-2].split()
            city = temp[len(temp)-1]
            d['city']=city
            d['state']=state
            d['zip']=zip
        except NoSuchElementException:
            address = ""
        try :
            phone = self.driver.find_element(By.XPATH,'//address[1]/a[1]').text
        except NoSuchElementException:
            phone =""
        url  = self.driver.current_url
        d['full_name']=full_name
        d['specality']=Speciality
        d['add_Speciality']=add_specality
        d['address']=address
        d['phone']=phone
        return d
        

ob = ProfileAssignment()

