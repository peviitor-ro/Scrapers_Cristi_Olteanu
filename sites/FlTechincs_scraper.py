#
# Company - > FlTechincs
# Link -> https://fltechnics.com/careers/?c-ctry=29#career-list
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_soup(url: str):
    session = requests.Session()
    response = session.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():
    soup_pages = get_soup(url='https://fltechnics.com/careers/?#career-list')
    nr_jobs = int(soup_pages.find('div', class_='info').find('span').text)
    nr_pages = int(nr_jobs / 5)
    return nr_pages


def get_jobs():

    list_jobs = []

    for page in range(1, get_pages() + 1, 1):

        soup = get_soup(url=f'https://fltechnics.com/careers/page/{page}/#career-list')
        jobs = soup.find_all('div', class_='row_col_wrap_12 col span_12 dark left career')

        for job in jobs:

            link = job.find('a')['href']
            title = job.find('a').text
            location = job.find('div', class_='asgc-list-col col-location').text.strip().split(', ')[1]
            city = job.find('div', class_='asgc-list-col col-location').text.strip().split(', ')[0]

            if location == 'Romania':
                list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "FlTechincs",
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


company_name = 'FlTechincs'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('FlTechincs',
                  'https://fltechnics.com/wp-content/uploads/2021/07/flt-logo-org.svg'
                  ))


