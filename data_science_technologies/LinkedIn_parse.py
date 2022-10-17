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

driver.implicitly_wait(1)

# Make a list to store final data
result = []

# find all job-postings on the current page 
def find_all_postings():
    all_postings = driver.find_elements(by = By.CLASS_NAME, value ='disabled ember-view job-card-container__link job-card-list__title')
    
    for posting in all_postings:
        posting.click()

        # Get job specification in text 
        job_details = driver.find_element(by = By.ID, value = 'job-details').text

        #Get a company group name 
        group_name = driver.find_element(by= By.CLASS_NAME, value = 'ember-view t-black t-normal').text
    
        # Append the result to our list 
        result.append({group_name, job_details})

        return result

# Creating a function to find and click on the next button
def find_new_button():

    # Find the button selection menue 
    button_selection = driver.find_element(by = By.CLASS_NAME, value = 'artdeco-pagination__pages artdeco-pagination__pages--number')

    # Find each button in the menue 
    all_buttons = button_selection.find_elements(by = By.TAG_NAME, value = 'li')

    # Loop through the buttons to find the current one
    for i in all_buttons:

        # Check if button has the current button class value 
        if i.get_attribute('class') == 'artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view':

            # When value has been found, we can try to index the next button from our list 
            try:
                next_button = all_buttons[all_buttons.index(i) + 1 ]

                button_object  = next_button.find_element(by= By.TAG_NAME, value = 'button')
                return button_object, True


            except:
                print(f'That was the last page , parsing has been finished.\n Totally parsed {len(result)} job posts')
                return None, False
        else:
            continue

stop_value = True
def main(result):
    while stop_value:
        result = find_all_postings()
        print(len(result))

        button , stop_value = find_new_button()

        if stop_value :
            button.click()
    df = pd.DataFrame(result)
    df.to_csv('LinkedIn_data')
    
    
