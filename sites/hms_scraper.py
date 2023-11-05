#
# Company - > caseware
# Link -> https://jobs.lever.co/caseware?location=Cluj%2C%20Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid


def get_jobs():

    list_jobs = []

    response = requests.get('https://career.hms-networks.com/#page-block-12397', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_='position-container filter-item')

    for job in jobs:

        link = 'https://career.hms-networks.com' + job.find('a', class_='position-title')['href']
        title = job.find('a', class_='position-title').text
        location = job.find('span', class_='location tag').text
        city = location.split(',')[0]
        try:
            job_type = job.find('div', style='margin-top: 0.5em').text
        except:
            job_type = 'on-site'

        if 'Romania' in location:
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "HMS",
                "country": "Romania",
                "city": city,
                "remote": job_type
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'HMS'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('HMS',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/HMS_logo.png/800px-HMS_logo.png?20210924132713'
                  ))