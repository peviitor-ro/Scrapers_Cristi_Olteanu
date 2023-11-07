#
#  Company - > ascom
# Link -> https://career.ascom.com/jobs?country=Romania&location=RO+Cluj-Napoca&query=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_jobs():

    list_jobs = []
    soup_jobs = get_soup('https://career.ascom.com/jobs?country=Romania&location=RO+Cluj-Napoca&query=')
    jobs = soup_jobs.find_all('li', class_='block-grid-item border border-block-base-text border-opacity-15 min-h-[360px] items-center justify-center rounded overflow-hidden relative z-career-job-card-image')

    for job in jobs:

        title = job.find('span', class_='text-block-base-link company-link-style')['title']
        link = job.find('a')['href']
        city = job.find('div', class_='mt-1 text-md').text.split()[-1]

        soup_job_type = get_soup(link)
        job_type = soup_job_type.find('dl', class_='md:max-w-[70%] mx-auto text-md gap-y-0 md:gap-y-5 flex flex-wrap flex-col md:flex-row company-links').text.split()[-1]

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "ascom",
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


company_name = 'ascom'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('ascom',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Logo_Ascom.svg/800px-Logo_Ascom.svg.png'
                  ))