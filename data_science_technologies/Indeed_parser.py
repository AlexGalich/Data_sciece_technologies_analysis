# Importing needed packages 
import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import time

# Creating needed headers for authorithation 
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
          'cookie': 'CTK=1gc55lmurgpd4802; RF="TFTzyBUJoNr6YttPP3kyivpZ6-9J49o-Uk3iY6QNQqKE2fh7FyVgtQ-jFr_4ohfEcEaFOJkBrWA="; _gcl_au=1.1.1167844270.1662326073; __ssid=4d65ee93b6a72352314bf5750d2cde8; SOCK="WqcZLBlqUXrv3C8dSW_An-z2vY4="; SHOE="aLFLNy3CHnmHg4JQSujd_PQnooGXY62ieyiHj8AAP4-RMzsFe1QRF13qLvNtfNMjXYFCZwfp5c1nzqzsNOwvHM_EOGaxBJOf1PQNZmc9CGFLT8qWgM35RcZzJ-_vWyy_Iq0KOIrCMtt34ZvlWdSYD2Za"; CO=DE; OptanonAlertBoxClosed=2022-10-07T20:01:18.844Z; LOCALE=de; indeed_rcc=LOCALE:CO:CTK; _ga=GA1.2.1206671310.1667573460; CSRF=memz63TwV0ivAfZmhrPkCtKg1XLYFpDE; SHARED_INDEED_CSRF_TOKEN=rSIkPeVUBDrcvtIBg9SaQRzgLsTGiJSU; MICRO_CONTENT_CSRF_TOKEN=xPXGmq5NW9yJYyQ6s2Ti88w64IDx6BCM; LC="co=DE"; _cfuvid=1S1sfZLo4Ky.UtTEDLknydQ_AWGgteMfW6MyqVgI.yk-1668170539297-0-604800000; __cf_bm=s.QOSsKtHidskt89MHWQNdDGiiABHP02klx2eV2lZfQ-1668173432-0-AXB7GbsRHmqq4BmRqVmRhwQqgaQ4IoA6Pxqwm2zBeiiDIZsH9yKaMy+GzBCTUyo8PpIMcrxwe1uLzfvSE6IokqA=; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Nov+11+2022+14%3A42%3A43+GMT%2B0100+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.37.0&isIABGlobal=false&hosts=&consentId=94f641ec-3736-4a58-84fc-20015f930371&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&AwaitingReconsent=false&geolocation=%3B'}
base_link = 'https://de.indeed.com'



# Create a funcion to send a request 
def make_request(link):
    time.sleep(1)
    r = requests.get(link, headers = headers)
    print(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')
    return soup  # Retruns a soup object 


def extract(soup):

    # Find all job listning objects 
    divs = soup.find_all('div', class_ = 'job_seen_beacon')

    # Loop through them to find title and job description 
    for item in divs:

        # Find and extention link to the full job description
        job_link = item.find('a').attrs['href']

        # Combine the extention with the base 
        full_link = base_link+job_link
        
        # Find the title 
        title = item.find('a').find('span').text
        
        # Try to access the main description
        try:
            job_description = make_request(full_link).find('div', id = 'jobDescriptionText').text.strip().replace('/n', '')
        except: 
            job_description = None

        # Saving title and description 
        job = {
            'title': title,
            'job_description': job_description
        }

        # Appending the dictionary to the main list
        job_list.append(job)
    
    return  

    

job_list = []
for i in range(1,80):

    url = f'https://de.indeed.com/jobs?q=Data+Science&l=Germany&start={i}0&pp=gQAPAAAAAAAAAAAAAAAB6aZWRQAqAQEBBwP4Dv2QdwDMoXJv0r_WrdKtZE-eaF-FHuXQu0G6_KTNwgGvd0Z9AAA&vjk=e5024ad803791f06'
    
    c = make_request(url)
    extract(c)
    print(len(job_list))

df = pd.DataFrame(job_list)
df.to_('Indeed_data')