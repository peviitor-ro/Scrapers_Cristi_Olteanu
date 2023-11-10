#
# Company - > OlxGroup
# Link -> https://jobs.eu.lever.co/olx/?
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_jobs():
    response = requests.get('https://jobs.eu.lever.co/olx',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    list_jobs = []

    jobs = soup.find_all('div',class_='posting')

    for job in jobs:
        link = job.find('a',class_='posting-title')['href']
        title = job.find('h5').text
        country = job.find('span',class_='sort-by-location posting-category small-category-label location').text.split(', ')[-1]
        location = job.find('span',class_='sort-by-location posting-category small-category-label location').text.split(', ')[0]

        if 'Remote' in location:
            city = 'Bucuresti'
            remote = 'remote'
        else:
            city = location
            remote = 'on-site'

        if country == 'Romania':
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "OlxGroup",
                "country": "Romania",
                "city": city,
                "remote": remote
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'OlxGroup'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('OlxGroup',
                  'https://seeklogo.com/images/O/olx-group-logo-D786F321B8-seeklogo.com.png'
                  ))