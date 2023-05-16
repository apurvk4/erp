from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import random
from sys import platform
import os ;
class feedback():
    def __init__(self) -> None:
        self.driver = None
        if platform == "linux" or platform == "linux2":
            options= ChromeOptions()
            cwd = os.getcwd()
            os.chdir(cwd)
            cwd = os.getcwd()
            cwd = "--user-data-dir="+os.path.join(cwd,"user-data")
            options.add_argument(cwd)
            options.add_argument('--log-level=3')
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))
        elif platform == "darwin":
            # OS X
            options= ChromeOptions()
            cwd = os.getcwd()
            os.chdir(cwd)
            cwd = os.getcwd()
            cwd = "--user-data-dir="+os.path.join(cwd,"user-data")
            options.add_argument(cwd)
            options.add_argument('--log-level=3')
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))
        elif platform == "win32":
            options  = EdgeOptions()
            cwd = os.getcwd()
            os.chdir(cwd)
            cwd = os.getcwd()
            cwd = "--user-data-dir="+os.path.join(cwd,"user-data")
            options.add_argument(cwd)
            options.add_argument('--log-level=3')
            options.add_argument("--start-maximized")
            self.driver = webdriver.Edge(options=options,service=EdgeService(EdgeChromiumDriverManager().install()))
        self.driver.get("https://erp.skit.ac.in/feedback/even2223")
        # sleep(30);
        self.last = False
        sleep(2)
    def findSection(self):
        base_path = "(//div[@id='hide-table'])["
        i =1
        while True : 
            try : 
                path = base_path + str(i)+"]"
                el = self.driver.find_element(By.XPATH,path)
                self.driver.execute_script("arguments[0].scrollIntoView()",el)
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
        mask  = False
        while True : 
            try : 
                path = ".//tr["+str(i)+"]"
                tr  = el.find_element(By.XPATH,path)
                b = None 
                if not(mask):
                    b = tr.find_element(By.XPATH,".//td[1]/b[1]")
                elif i == 1:
                    b= tr
                self.driver.execute_script("arguments[0].scrollIntoView()",head)
                self.driver.execute_script('''window.scrollBy(60, -window.innerHeight)''')
                self.fillfeedback(tr)
                i+=1
                head = tr
                self.driver.execute_script("arguments[0].scrollIntoView()",b)
            except NoSuchElementException as e:
                if (i==1 and not mask) : 
                    mask=True
                    continue
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
            except (NoSuchElementException,ElementClickInterceptedException)  as e:
                break
    def fillDropDown(self,el):
        path = ".//div[1]/input[1]"
        el1 = el.find_element(By.XPATH,path)
        self.driver.execute_script("arguments[0].click();",el1)
        num = random.randint(1,5)
        el1.send_keys(str(num))
        el1.send_keys(Keys.ENTER)
if __name__ == "__main__":
    print("\x1b[6;30;42m Have You Run this program before and Logged in with your credentials ? \x1b[0m")
    inp = input("type Y or N to confirm Yes or No : ")
    if(inp == "Y" or inp == "y"):
        ob = feedback()
        sleep(5);
        ob.findSection()
    elif (inp == 'n' or inp == 'n') :
        print("\x1b[6;30;42m Please log in with your credentials. After logging in, manually close the browser, and then run this program again to continue. \x1b[0m")
        sleep(4);
        ob = feedback()
        sleep(120);
   