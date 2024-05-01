#
#  Company - > hartrodt
# Link -> https://www.hartrodt.com/career/open-positions/p1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county
from _validate_city import validate_city


def get_soup(url):
    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():
    pages = int(get_soup('https://www.hartrodt.com/career/open-positions/p1'
                         ).find('span', class_='m-pagination__content').text.split()[-1])
    return pages


def get_jobs():

    job_list = []

    for page in range(1, get_pages()+1, 1):

        jobs = get_soup(f'https://www.hartrodt.com/career/open-positions/p{page}'
                        ).find_all('div', class_='m-listicle')
        for job in jobs:
            title = job.find('a', class_='m-listicle__link')['title']
            link = job.find('a', class_='m-listicle__link')['href']
            city = validate_city(job.find('h4', class_='m-listicle__subline').text.split(',')[0].strip())
            country = job.find('h4', class_='m-listicle__subline').text.split(',')[-1].strip()

            if 'Romania' in country:
                job_list.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "hartrodt",
                    "country": "Romania",
                    "city": city,
                    "county": get_county(city),
                    "remote": 'on-site'
                })
    return job_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'hartrodt'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hartrodt',
                  'https://logowik.com/content/uploads/images/a-hartrodt5150.logowik.com.webp'
                  ))