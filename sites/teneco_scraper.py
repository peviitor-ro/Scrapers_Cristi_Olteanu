#
# Company - > teneco
# Link ->https://jobs.tenneco.com/search/?createNewAlert=false&q=&locationsearch=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_num_pages():

    soup_pages = get_soup('https://jobs.tenneco.com/search/?createNewAlert=false&q=&locationsearch=Ro')
    num_pages = soup_pages.find('span', class_='srHelp').text.split('of')[-1].strip()
    return int(num_pages)


def get_jobs():

    list_jobs = []

    for page in range(0, get_num_pages()*10, 10):

        soup_jobs = get_soup(f'https://jobs.tenneco.com/search/?q=&locationsearch=Romania&startrow={page}')
        jobs = soup_jobs.find_all('tr', class_='data-row')

        for job in jobs:
            link = 'https://jobs.tenneco.com/'+job.find('a', class_='jobTitle-link')['href']
            title = job.find('a', class_='jobTitle-link').text
            city = job.find('span', class_='jobLocation').text.split(', ')[-2].strip()
            country = job.find('span', class_='jobLocation').text.split(', ')[-1].split()[0]

            if country != 'RO':
                cities = get_soup(link).find_all('span', class_='jobGeoLocation')
                for item in cities:
                    if 'RO' in item.text:
                        city = item.text.split(',')[0].strip('\n')

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "teneco",
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


company_name = 'teneco'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('teneco',
                  'https://rmkcdn.successfactors.com/8fba3c45/d59e3e3d-da03-4939-b876-e.jpg'
                  ))
