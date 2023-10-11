#
# Company - > PayU
# Link -> https://corporate.payu.com/job-board/?location%5B%5D=bucharest-romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid

def get_jobs():

    req = requests.get('https://corporate.payu.com/job-board/?location%5B%5D=bucharest-romania',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text,'lxml')
    jobs = soup.find_all('li',class_='job-entry')

    list_jobs=[]

    for job in jobs:

        link = job.find('a',class_='title')['href']
        title = job.find('h3').text
        city = job.find('a').text.split(',')[-2].split()[-1]

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "PayU",
            "country": "Romania",
            "city": city,
        })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'PayU'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('PayU',
                  'https://corporate.payu.com/wp-content/themes/global-website/assets/src/images/payu-logo.svg'
                  ))

