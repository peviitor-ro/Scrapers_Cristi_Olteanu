#
#  Company - > Pearson
# Link -> https://pearson.jobs/jobs/?location=Romania&r=25
#

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid

def get_jobs():

    list = []

    req = requests.get('https://pearson.jobs/jobs/?location=Romania&r=25',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, 'lxml')
    jobs = soup.find_all('li', class_='direct_joblisting with_description')

    for job in jobs:
        link = job.find('a')['href']
        title = job.find('span').text
        location = job.find('span', class_='hiringPlace').text.strip().split(',')[0]

        if location == 'Romania':
            location = 'Bucuresti'
            remote = 'remote'
        else:
            remote = 'on-site'

        list.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": 'https://pearson.jobs'+link,
            "company": "Pearson",
            "country": "Romania",
            "city": location,
            "remote": remote
        })

    return list

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Pearson'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Pearson',
                  'https://logowik.com/content/uploads/images/pearson-plc1129.jpg'
                  ))
