#
#  Company - > superbet
# Link -> https://boards.eu.greenhouse.io/superbet
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():

    list_jobs = []

    response = requests.get('https://boards.eu.greenhouse.io/superbet',
                            headers=DEFAULT_HEADERS)

    soup = BeautifulSoup(response.text,'lxml')
    jobs = soup.find_all('div',class_='opening')

    for job in jobs:
        link = 'https://boards.eu.greenhouse.io/' + job.find('a')['href']
        title = job.find('a').text
        country = job.find('span',class_='location').text

        if 'Romania' in country:
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "SuperBet",
                "country": "Romania",
                "city": 'Bucuresti',
            })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'SuperBet'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('SuperBet',
                  'https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/134/810/resized/favicon.png?1673612131'
                  ))