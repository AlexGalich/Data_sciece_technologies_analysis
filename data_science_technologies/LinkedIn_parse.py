# Import required packages
from gettext import find
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# Assign the main link to the website 
# saving driver to a local variable to than access web sites via chromia 
PATH = r"C:\selenium_drivers\chromedriver.exe"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3315497151&f_E=1%2C2&geoId=101282230&keywords=data%20scientist&location=Germany&refresh=true')



driver.implicitly_wait(15)



# Make a list to store final data
result = []

# find all job-postings on the current page 
def find_all_postings():
    all_postings = driver.find_element(by = By.CLASS_NAME, value ='jobs-search__results-list').find_elements(by = By.TAG_NAME, value = 'li')
    
    for posting in all_postings:

        # click on individual posting
        posting.click()

        # Find show more button to get full job description
        show_more = driver.find_element(by= By.CLASS_NAME, value = 'show-more-less-html__button show-more-less-html__button--more')
        show_more.click()

        # Get job specification in text 
        job_details = driver.find_element(by = By.CLASS_NAME, value = 'show-more-less-html__markup').text

        #Get a company group name 
        group_name = driver.find_element(by= By.CLASS_NAME, value = 'topcard__org-name-link topcard__flavor--black-link').text
    
        # Append the result to our list 
        result.append({group_name, job_details})

        return result

# Creating a function to find and click on the next button
def scroll_downer(driver):
    for i in range(200):
        
        driver.execute_script("window.scrollTo(0,540 )") 
        print('going')
        try:
            next_page_button  = driver.find_element(by = By.CLASS_NAME , value = 'infinite-scroller__show-more-button infinite-scroller__show-more-button--visible')
            next_page_button.click()
        except:
            continue
    return driver 


stop_value = True

def main(result):
    scroll_downer(driver)
    result = find_all_postings
    df = pd.DataFrame(result)
    df.to_csv('LinkedIn_data')
    
    
