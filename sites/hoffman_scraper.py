#
# Company - > Hoffman
# Link -> https://career.hoffmann-group.com/job-offers.html
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid


def get_jobs():
    list_jobs = []

    response = requests.get('https://career.hoffmann-group.com/job-offers.html',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')

    jobs = soup.find_all('div',class_='joboffer_container')

    for job in jobs:
        city = job.find('a',class_='joboffer_maplink').text.split(' - ')[1]
        link = job.find('a')['href']
        title = job.find('a').text
        country = job.find('a',class_='joboffer_maplink').text.split(' - ')[0]

        if 'RO' in country:
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Hoffman",
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


company_name = 'Hoffman'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Hoffman',
                  'https://www.karrieretag.org/wp-content/uploads/2022/04/hoffmann-group-logo.png'
                  ))

