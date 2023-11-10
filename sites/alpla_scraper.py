#
#  Company - > alpla
# Link -> https://career.alpla.com/ro/jobs
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_soup(url):
    session = requests.Session()
    response = session.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():

    soup_pages = get_soup('https://career.alpla.com/en/jobs?page=')
    nr_jobs = int(soup_pages.find('h3').text.split()[0])
    pages = int(nr_jobs/30)
    if nr_jobs % 30 > 0:
        pages += 1

    return pages


def get_jobs():

    list_jobs = []

    for page in range(0, get_pages(), 1):

        soup_jobs = get_soup(f'https://career.alpla.com/en/jobs?page={page}')
        jobs = soup_jobs.find_all('tr')

        for job in jobs:
            country = job.findNext('td', attrs={'class': 'views-field views-field-field-location-country'}).find('a').text
            if country == 'Romania':

                text = job.findNext('td', class_='views-field views-field-title')
                link = 'https://career.alpla.com' + text.find('a')['href']
                title = text.find('a').text
                city = job.findNext('td', class_='views-field views-field-field-location-city').find('a').text

                if 'Bucharest' in city:
                    city = 'Bucharest'

                list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "alpla",
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


company_name = 'alpla'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('alpla',
                  'https://career.alpla.com/themes/custom/career/assets/images/logo-family.svg'
                  ))
