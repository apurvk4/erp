from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import os ;
class feedback():
    def __init__(self,value) -> None:
        options= ChromeOptions()
        cwd = os.getcwd()
        os.chdir(cwd)
        cwd = os.getcwd()
        cwd = "--user-data-dir="+cwd
        options.add_argument(cwd)
        # options.add_argument('--headless')
        options.add_argument('--log-level=3')
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--ignore-certificate-errors')
        self.points=value
        self.driver= webdriver.Chrome(options=options)
        self.driver.get("https://erp.skit.ac.in/feedback/odd2122")
        self.last = False
        sleep(5)
    def findSection(self):
        base_path = "(//div[@id='hide-table'])["
        i =1
        while True : 
            try : 
                path = base_path + str(i)+"]"
                el = self.driver.find_element(By.XPATH,path)
                self.fillFacultyList(el)
                i+=1
            except  NoSuchElementException as e:
                if not(self.last) and i != 1 :
                    self.last=True
                    i=i-1
                else: 
                    break
    def fillFacultyList(self,el):
        i= 1 
        head = el.find_element(By.XPATH,".//div[1]/div[4]/div[2]/table[1]/thead[1]")
        el = el.find_element(By.XPATH,".//../tbody[1]")
        while True : 
            try : 
                path = ".//tr["+str(i)+"]"
                tr  = el.find_element(By.XPATH,path)
                b = tr.find_element(By.XPATH,".//td[1]/b[1]")
                self.driver.execute_script("arguments[0].scrollIntoView()",head)
                self.driver.execute_script('''window.scrollBy(60, -window.innerHeight)''')
                self.fillfeedback(tr)
                i+=1
                head = tr
                self.driver.execute_script("arguments[0].scrollIntoView()",b)
            except NoSuchElementException as e:
                break
    def fillfeedback(self,tr):
        base_path = ".//td["
        i = None
        if self.last : 
            i = 1 
        else : 
            i = 3
        while True : 
            path = base_path+str(i)+"]/div[1]/a[1]"
            try :
                a = tr.find_element(By.XPATH,path)
                a.click()
                dropdown =WebDriverWait(self.driver,timeout=10).until(lambda d:d.find_element(By.ID,"select2-drop"))
                self.fillDropDown(dropdown)
                i+=1
                sleep(0.5)
            except NoSuchElementException  as e:
                break
    def fillDropDown(self,el):
        path = ".//div[1]/input[1]"
        el1 = el.find_element(By.XPATH,path)
        self.driver.execute_script("arguments[0].click();",el1)
        el1.send_keys(str(self.points))
        el1.send_keys(Keys.ENTER)
if __name__ == "__main__":
    ob = feedback(int(input("\x1b[6;30;42m feedback score : \x1b[0m")))
    ob.findSection()
   