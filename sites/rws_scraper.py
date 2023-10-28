#
# Company - > rws
# Link -> https://globalcareers-rws.icims.com/jobs/search?ss=1&searchLocation=13526--
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_jobs():

    list_jobs = []

    querystring = {"ss": "1", "in_iframe": "1", "searchLocation": "13526--"}

    response = requests.get('https://globalcareers-rws.icims.com/jobs/search#iCIMS_Header',
                            headers=DEFAULT_HEADERS,
                            params=querystring)

    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='row')

    for job in jobs:
        text = job.find('a', class_='iCIMS_Anchor')

        if text is not None:
            title = text['title'].split('-')[1]
            link = text['href']

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "rws",
                "country": "Romania",
                "city": 'Cluj-Napoca',
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'rws'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('rws',
                  'https://c-13850-20230914-www-rws-com.i.icims.com/media/images/Artboard-1_tcm228-187294.svg?v=NjM4MjcwODY1NTA3MTQyMTkw'
                  ))
