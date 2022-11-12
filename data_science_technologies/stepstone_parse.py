import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'cookie':'pjps=1; __ssid=4d65ee93b6a72352314bf5750d2cde8; SOCK="WqcZLBlqUXrv3C8dSW_An-z2vY4="; SHOE="aLFLNy3CHnmHg4JQSujd_PQnooGXY62ieyiHj8AAP4-RMzsFe1QRF13qLvNtfNMjXYFCZwfp5c1nzqzsNOwvHM_EOGaxBJOf1PQNZmc9CGFLT8qWgM35RcZzJ-_vWyy_Iq0KOIrCMtt34ZvlWdSYD2Za"; CO=DE; mobbcpc=1; OptanonAlertBoxClosed=2022-10-07T20:01:18.844Z; RSJC=a87c6e8dcb0e938d:c9d554bc5ab01618:2abcf4eb5aaa7a87:76dd0374ff95439d:b78322e40cddf4dc:e1e7f303e9505abc; CSRF=mS4efLDunVDo3ocEN7jXvH30ntKnWQcw; _cfuvid=F.rYgOQUqDfdlxemn1Uf4zCrqPrS7Amn2qavbitZrsc-1666075246883-0-604800000; INDEED_CSRF_TOKEN=etpCydEU1ErG5If2eWzSy6yjqqC7ifXc; CO=DE; LOCALE=uk; indeed_rcc="LOCALE:PREF:LV:CTK:CO:UD:RQ"; UD="LA=1665349730:LV=1665172178:CV=1665349380:TS=1662326070"; SHARED_INDEED_CSRF_TOKEN=etpCydEU1ErG5If2eWzSy6yjqqC7ifXc; LOCALE=de; MICRO_CONTENT_CSRF_TOKEN=g4JjJaOsmVrl9Tnin6f2hRLtTCO2Zmf8; gonetap=1; LANG=de; PREF="TM=1666092772981:LD=de:L=Germany"; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+18+2022+13%3A33%3A24+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.37.0&isIABGlobal=false&hosts=&consentId=94f641ec-3736-4a58-84fc-20015f930371&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&AwaitingReconsent=false&geolocation=%3B; __cf_bm=sLLKX8bXdgjCrYWgnPdA48JT.7qzEriojTnNlzmaIEM-1666094417-0-AWTTEt9OQWgfkf+b2Pxk+HbYPpGxK24NeX4nXsiRkdGd8EYMWWp87FNyL1VeULntLWJ8PY6DSq/YKJcpW6dBulo=; LC="co=DE"; LV="LA=1666094561:LV=1666081349:CV=1666088946:TS=1662326070"; ROJC=75212012b4438e03:5a5f5b36c691062e:3ccf22bbda7af836:9376b8ea8dede4a0:769461f9cf5d9888:135ef91e6808e941:71857f8dacccc310:a234d105a31831dc:768ad584bba0cf5c:c43497ce5bf47f76; RCLK=jk=75212012b4438e03&tk=1gfldt7lt2ek5001&from=web&rd=VwIPTVJ1cTn5AN7Q-tSqGRXGNe2wB2UYx73qSczFnGU&qd=RnZhMybXSk4M3QtTVGXWoUo2x18JxrC6fD6X4HE39WqGiC6Uo7fLyX9gXjBsnq6RtpkjM0hihmiCIYIuM7geNnN9xwMnuCAoNVciDCbeF3I&ts=1666092801725&sal=0; jaSerpCount=13; RQ="q=Data+Scientist&l=Germany&ts=1666094626380&pts=1666081349914:q=Germany+Data+Scientist&l=&ts=1666081434966:q=Working+Student+Data+Analysis&l=Hamburg&ts=1665349730919&pts=1665169071109:q=Data+Science+Student&l=Hamburg&ts=1665349718976:q=Working+student+data&l=Hamburg&ts=1665349716130:q=Data+Science+Student&l=&ts=1665349380500:q=Working+Student+Data+Analysis&l=&ts=1665173512595:q=Data+Analyst+Part+Time&l=&ts=1662326114631"; JSESSIONID=2B624C133ADED2A1BA50B1745D1FC6AB; PPID=eyJraWQiOiJlNDE1NGIxOS00ZDE0LTRhM2UtOTg4MS00M2QyYzljYzQ1YWUiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJiZWNkNjU2ZjNkNmRmMDY5IiwiYXVkIjoiYzFhYjhmMDRmIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF1dGgiOiJnb29nbGUiLCJjcmVhdGVkIjoxNjUzNDc0ODUwMDAwLCJyZW1fbWUiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9zZWN1cmUuaW5kZWVkLmNvbSIsImV4cCI6MTY2NjA5NjQyNywiaWF0IjoxNjY2MDk0NjI3LCJsb2dfdHMiOjE2NjIzMjYxMDAxMDcsImVtYWlsIjoiYWxla3NhbmRyZ2FsaWMyNTA0QGdtYWlsLmNvbSJ9.AbH9hvkmhDxP1V6yMVbIj0a63-a9-U5mRs20f-1aWHi7EtLuo3jlVKqDKHBZ2QnuzhPuYXhjMREQEWZpSoSPLQ'}


def make_request(link):
    
    r = requests.get(link, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def extract(page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'cookie':'pjps=1; __ssid=4d65ee93b6a72352314bf5750d2cde8; SOCK="WqcZLBlqUXrv3C8dSW_An-z2vY4="; SHOE="aLFLNy3CHnmHg4JQSujd_PQnooGXY62ieyiHj8AAP4-RMzsFe1QRF13qLvNtfNMjXYFCZwfp5c1nzqzsNOwvHM_EOGaxBJOf1PQNZmc9CGFLT8qWgM35RcZzJ-_vWyy_Iq0KOIrCMtt34ZvlWdSYD2Za"; CO=DE; mobbcpc=1; OptanonAlertBoxClosed=2022-10-07T20:01:18.844Z; RSJC=a87c6e8dcb0e938d:c9d554bc5ab01618:2abcf4eb5aaa7a87:76dd0374ff95439d:b78322e40cddf4dc:e1e7f303e9505abc; CSRF=mS4efLDunVDo3ocEN7jXvH30ntKnWQcw; _cfuvid=F.rYgOQUqDfdlxemn1Uf4zCrqPrS7Amn2qavbitZrsc-1666075246883-0-604800000; INDEED_CSRF_TOKEN=etpCydEU1ErG5If2eWzSy6yjqqC7ifXc; CO=DE; LOCALE=uk; indeed_rcc="LOCALE:PREF:LV:CTK:CO:UD:RQ"; UD="LA=1665349730:LV=1665172178:CV=1665349380:TS=1662326070"; SHARED_INDEED_CSRF_TOKEN=etpCydEU1ErG5If2eWzSy6yjqqC7ifXc; LOCALE=de; MICRO_CONTENT_CSRF_TOKEN=g4JjJaOsmVrl9Tnin6f2hRLtTCO2Zmf8; gonetap=1; LANG=de; PREF="TM=1666092772981:LD=de:L=Germany"; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+18+2022+13%3A33%3A24+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.37.0&isIABGlobal=false&hosts=&consentId=94f641ec-3736-4a58-84fc-20015f930371&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&AwaitingReconsent=false&geolocation=%3B; __cf_bm=sLLKX8bXdgjCrYWgnPdA48JT.7qzEriojTnNlzmaIEM-1666094417-0-AWTTEt9OQWgfkf+b2Pxk+HbYPpGxK24NeX4nXsiRkdGd8EYMWWp87FNyL1VeULntLWJ8PY6DSq/YKJcpW6dBulo=; LC="co=DE"; LV="LA=1666094561:LV=1666081349:CV=1666088946:TS=1662326070"; ROJC=75212012b4438e03:5a5f5b36c691062e:3ccf22bbda7af836:9376b8ea8dede4a0:769461f9cf5d9888:135ef91e6808e941:71857f8dacccc310:a234d105a31831dc:768ad584bba0cf5c:c43497ce5bf47f76; RCLK=jk=75212012b4438e03&tk=1gfldt7lt2ek5001&from=web&rd=VwIPTVJ1cTn5AN7Q-tSqGRXGNe2wB2UYx73qSczFnGU&qd=RnZhMybXSk4M3QtTVGXWoUo2x18JxrC6fD6X4HE39WqGiC6Uo7fLyX9gXjBsnq6RtpkjM0hihmiCIYIuM7geNnN9xwMnuCAoNVciDCbeF3I&ts=1666092801725&sal=0; jaSerpCount=13; RQ="q=Data+Scientist&l=Germany&ts=1666094626380&pts=1666081349914:q=Germany+Data+Scientist&l=&ts=1666081434966:q=Working+Student+Data+Analysis&l=Hamburg&ts=1665349730919&pts=1665169071109:q=Data+Science+Student&l=Hamburg&ts=1665349718976:q=Working+student+data&l=Hamburg&ts=1665349716130:q=Data+Science+Student&l=&ts=1665349380500:q=Working+Student+Data+Analysis&l=&ts=1665173512595:q=Data+Analyst+Part+Time&l=&ts=1662326114631"; JSESSIONID=2B624C133ADED2A1BA50B1745D1FC6AB; PPID=eyJraWQiOiJlNDE1NGIxOS00ZDE0LTRhM2UtOTg4MS00M2QyYzljYzQ1YWUiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJiZWNkNjU2ZjNkNmRmMDY5IiwiYXVkIjoiYzFhYjhmMDRmIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF1dGgiOiJnb29nbGUiLCJjcmVhdGVkIjoxNjUzNDc0ODUwMDAwLCJyZW1fbWUiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9zZWN1cmUuaW5kZWVkLmNvbSIsImV4cCI6MTY2NjA5NjQyNywiaWF0IjoxNjY2MDk0NjI3LCJsb2dfdHMiOjE2NjIzMjYxMDAxMDcsImVtYWlsIjoiYWxla3NhbmRyZ2FsaWMyNTA0QGdtYWlsLmNvbSJ9.AbH9hvkmhDxP1V6yMVbIj0a63-a9-U5mRs20f-1aWHi7EtLuo3jlVKqDKHBZ2QnuzhPuYXhjMREQEWZpSoSPLQ'}
    url = f'https://www.stepstone.de/jobs/data-scientist/in-germany?radius=30&page={page}'
    
    r = requests.get(url, headers = headers)
    print(r.status_code)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup
base_link = 'https://www.stepstone.de'
def transfortm(soup):
    divs = soup.find_all('div', class_ = 'Wrapper-sc-11673k2-0 cmgNOQ')
    for item in divs:
        job_link = item.find('a', class_ = 'resultlist-12iu5pk').attrs['href']
        
        full_link = base_link+job_link
    
        

        title = item.find('a', class_ = 'resultlist-12iu5pk').text

        

        try:
            job_description = make_request(full_link).find('div', class_= 'js-app-ld-ContentBlock').text.strip().replace('/n', '')
        except: 
            job_description =None 

        
        job = {
            'title': title,
            'job_description': job_description
        }

        job_list.append(job)
    
    return

    

job_list = []
for i in range(35):
    
    c = extract(i)
    transfortm(c)
    print(len(job_list))

df = pd.DataFrame(job_list)
df.to_csv('StepStone_data')
