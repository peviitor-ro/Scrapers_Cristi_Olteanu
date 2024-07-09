#
#  Company - > Pearson
# Link -> https://pearson.jobs/jobs/?location=Romania&r=25
#

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county


def get_jobs():

    job_list = []

    req = requests.get('https://pearson.jobs/jobs/?location=Romania&r=25', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, 'lxml')
    jobs = soup.find_all('li', class_='direct_joblisting with_description')

    for job in jobs:
        link = job.find('a')['href']
        title = job.find('span').text
        city = job.find('span', class_='hiringPlace').text.strip().split(',')[0]

        if city == 'Romania':
            city = 'Bucuresti'
            remote = 'remote'
        else:
            remote = 'hybrid'

        job_list.append({
            "job_title": title,
            "job_link": 'https://pearson.jobs'+link,
            "company": "Pearson",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": remote
        })

    return job_list


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
