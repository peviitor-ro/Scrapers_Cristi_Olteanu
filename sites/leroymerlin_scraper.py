#
#  Company - > leroymerlin
# Link -> https://job.leroymerlin.ro/jobs
#
import requests
from bs4 import BeautifulSoup
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo


def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():

    soup_pages = get_soup('https://job.leroymerlin.ro/jobs')
    nr_jobs = int(soup_pages.find('span', class_='text-lg font-medium').text.split()[0])
    pages = int(nr_jobs/20)
    if nr_jobs % 20 > 0:
        pages += 1
    return pages


def get_jobs():

    list_jobs = []

    for page in range(1, get_pages()+1, 1):
        soup_jobs = get_soup(f'https://job.leroymerlin.ro/jobs?page={page}')

        jobs = soup_jobs.find_all('a', class_='block h-full w-full hover:bg-company-primary-text hover:bg-opacity-3 overflow-hidden group')

        for job in jobs:
            link = job.get('href')
            title = job.find('span', class_='text-block-base-link company-link-style').text
            location = job.find('div', class_='mt-1 text-md').text.split('·')[1].strip()
            if 'Târgu Mureș' in location:
                city = 'Târgu-Mureș'
            elif 'Cluj' in location:
                 city = 'Cluj-Napoca'
            else:
                city = location.split()[0]

            try:
                job_type = job.find('span',class_='inline-flex items-center gap-x-2').text.split()[-1]
            except:
                job_type = 'on-site'

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "LeroyMerlin",
                "country": "Romania",
                "city": city,
                "remote": job_type
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'LeroyMerlin'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('LeroyMerlin',
                  'https://logowik.com/content/uploads/images/leroy-merlin8331.jpg'
                  ))