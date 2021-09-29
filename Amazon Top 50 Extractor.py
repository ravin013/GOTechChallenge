import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import unittest
import pandas as pd

# Create log
logFilePath = "logs/default.log"
logLevel = logging.DEBUG 

# This method configures logging to a file at logFilePath with a level of logLevel
logging.basicConfig(level=logLevel)

# Create messages for different logs
logging.debug("Logging is configured - Log Level %s , Log File: %s",str(logLevel),logFilePath) 
logging.info("Informational log")
logging.warn("There is a warning")
logging.error("There is an error")

# Access the amazon bestsellers page
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.amazon.com')
bestseller = driver.find_element_by_xpath('//*[@id="nav-xshop"]//a[contains(text(),"Best Sellers")]')

bestseller.click()
driver.implicitly_wait(5)

# Create a list of all of the departments on the page   
driver.switch_to.window(driver.window_handles[0])
html_list = driver.find_element_by_xpath('//body/div/div/div/div/div/div/div/div/div/div/ul[1]')
departments = html_list.find_elements_by_tag_name("li")
department_names = []
for department in departments:
    department_names.append(department.text)

# Remove 'any department' from the list so the driver doesn't click on it
department_names.remove('Any Department')

# Iterate through all of the departments and save the title, rating, and price for the top 50 products
data = []
for department_name in department_names:
    try:
        driver.find_element_by_link_text(department_name).click()
        driver.implicitly_wait(5)
        root = driver.find_element_by_id("zg-ordered-list")
        departments1=root.find_elements_by_tag_name("li")
        data_dict = {}
        
        for department in departments1:
            print(department, type(department))
            product = department.text.split('\n')

            
            if len(product) == 3:
                print(product)                 
                data_dict['Name'] = product[1]
                data_dict['Price'] = product[2]
                data_dict['Department'] = department_name
                data.append(data_dict)
                data_dict = {}

            elif len(product) == 4:
                print(product)
                pNum1 = product[0]
                pNum2 = pNum1.split('#')[1]

                i = product[2].replace(",","")
                j = i.isdigit()
                k = i.isalpha()
                
                if j:
                    ratings1 = driver.find_element_by_xpath('//li[' + pNum2 + ' ]//span[1]//div[1]//span[1]//div[1]//a[1]//i[1]')
                    r2 = ratings1.get_attribute('innerHTML')
                    r3 = r2[25:43]
                    data_dict['Name'] = product[1]
                    data_dict['Rating'] = r3
                    data_dict['Price'] = product[3]
                    data_dict['Department'] = department_name
                    data.append(data_dict)
                    data_dict = {}                
                else:  
                    i = isinstance(product[2],int)                  
                    data_dict['Name'] = product[1]
                    data_dict['Price'] = product[3]
                    data_dict['Department'] = department_name
                    data.append(data_dict)
                    data_dict = {}
               
        
            elif len(product) == 5:
                print(product)
                pNum1 = product[0]
                pNum2 = pNum1.split('#')[1]
                l = product[3].replace(",","")
                m = l.isdigit()
                n = l.isalpha()

                if m:
                    ratings1 = driver.find_element_by_xpath('//li[' + pNum2 + ']//span[1]//div[1]//span[1]//div[2]//a[1]//i[1]')
                    r2 = ratings1.get_attribute('innerHTML')
                    r3 = r2[25:43]
                    data_dict['Rating'] = r3
                    data_dict['Name'] = product[1]
                    data_dict['Price'] = product[4]
                    data_dict['Department'] = department_name
                    data.append(data_dict)
                    data_dict = {}
                else:                    
                    data_dict['Name'] = product[1]
                    data_dict['Price'] = product[4]
                    data_dict['Department'] = department_name
                    data.append(data_dict)
                    data_dict = {}
                

            elif len(product) == 6:
                print(product)
                pNum1 = product[0]
                pNum2 = pNum1.split('#')[1]
                p = product[3].replace(",","")
                q = p.isdigit()
                r = p.isalpha()
                
                if q:
                    ratings1 = driver.find_element_by_xpath('//li[' + pNum2 + ']//span[1]//div[1]//span[1]//div[2]//a[1]//i[1]')
                    r2 = ratings1.get_attribute('innerHTML')
                    r3 = r2[25:43]
                    data_dict['Rating'] = r3
                    data_dict['Name'] = product[1]
                    data_dict['Price'] = product[5]
                    data_dict['Department'] = department_name
                    data.append(data_dict)
                    data_dict = {}
                else:                    
                    data_dict['Name'] = product[1]
                    data_dict['Price'] = product[5]
                    data_dict['Department'] = department_name
                    data.append(data_dict)
                    data_dict = {}
            else:
             print(product)                 
             data_dict['Name'] = 'Item no longer available'                
             data_dict['Department'] = department_name
             data.append(data_dict)
             data_dict = {}      

        driver.back()
        driver.implicitly_wait(5)
        
    except NoSuchElementException:
        driver.back()

# Save the data into a dataframe and load into csv
df = pd.DataFrame(data)
print(df)
df.to_csv("results.csv")

# Test cases
class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\\Chrome Driver\\chromedriver.exe")
        print("Browser Opened")
    def test_open_amazon(self):
        self.driver.get('https://www.amazon.com/')
        print("Opening Amazon.com")
    def test_click_bestseller(self):
        driver.get('https://www.amazon.com')
        bestseller = driver.find_element_by_xpath('//*[@id="nav-xshop"]//a[contains(text(),"Best Sellers")]')
        bestseller.click()
        driver.implicitly_wait(5)
        print("Clicking bestseller link")
    def tearDown(self):
        self.driver.quit()
        print("Browser closed")
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)