#
# Company - > Lenovo
# Link -> https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016749%5D&13036_format=6621&listFilterMode=1&jobRecordsPerPage=10&sort=relevancy
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():
    list_jobs = []

    req = requests.get(
        'https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016749%5D&13036_format=6621&listFilterMode=1&jobRecordsPerPage=10&sort=relevancy',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, 'lxml')

    jobs = soup.find_all('div', class_='article__header')

    for job in jobs:
        link = job.find('a')['href']
        title = job.find('a').text.strip()
        city = job.find('div',class_='article__header__text__subtitle').find('span').text.strip().split(', ')[-1]
        location = job.find('div',class_='article__header__text__subtitle').find('span').text.strip().split(', ')[-0]

        if location == 'Romania':
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Lenovo",
                "country": "Romania",
                "city": city
            })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Lenovo'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Lenovo',
                  'https://static.lenovo.com/fea/images/lenovo-logo-red.png'
                  ))