#
# Company - > Lenovo
# Link -> https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016749%5D&13036_format=6621&listFilterMode=1&jobRecordsPerPage=10&sort=relevancy
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():
    list_jobs = []

    page = 0
    flag = True

    while flag:

        req = requests.get(
            f'https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016749%5D&13036_format=6621&listFilterMode=1&jobSort=relevancy&jobRecordsPerPage=10&jobOffset={page}&sort=relevancy',
            headers=DEFAULT_HEADERS)
        soup = BeautifulSoup(req.text, 'lxml')
        jobs = soup.find_all('div', class_='article__header')

        for job in jobs:
            text_info = job.find('h3', class_="article__header__text__title article__header__text__title--4")
            if text_info is not None:
                link = job.find('a')['href']
                title = text_info.text.strip()

                list_jobs.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "Lenovo",
                    "country": "Romania",
                    "city": 'Bucuresti',
                    })
            else:
                flag = False
        page += 10
    return list_jobs
get_jobs()

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