#
# Company - > salesconsulting
# Link ->https://salesconsulting.teamtailor.com/jobs?page=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import uuid
from bs4 import BeautifulSoup
import requests


def get_soup(url):

    session = requests.Session()
    response = session.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_nr_pages():

    soup_pages = get_soup('https://salesconsulting.teamtailor.com/jobs?page=')
    nr_jobs = int(soup_pages.find('span', class_='text-lg font-medium').text.split()[0])
    nr_pages = int(nr_jobs/20)
    if nr_jobs % 20 > 0:
        nr_pages += 1

    return nr_pages


def get_jobs():
    list_jobs = []

    for page in range(1, get_nr_pages() + 1, 1):

        soup_jobs = get_soup(f'https://salesconsulting.teamtailor.com/jobs?page={page}')
        jobs = soup_jobs.find_all('li', class_='w-full')

        for job in jobs:
            text = job.find('a',
                            class_='flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded')

            if text is not None:
                link = text['href']
                title = job.find('span', class_='text-block-base-link sm:min-w-[25%] sm:truncate company-link-style')[
                    'title']
                job_type = job.find('div', class_='mt-1 text-md').text.split('·')[-1].strip().split()[-1]

                if 'hibrid' in job_type.lower() or 'remote' in job_type.lower():
                    city = job.find('div', class_='mt-1 text-md').text.split('·')[-2].strip()
                else:
                    city = job_type
                    job_type = 'on-site'

                if 'multiple' in city.lower():
                    soup_city = get_soup(link)
                    city = soup_city.find('dl',
                                          class_='md:max-w-[70%] mx-auto text-md gap-y-0 md:gap-y-5 flex flex-wrap flex-col md:flex-row company-links'
                                          ).text.split('Locații')[1].split('Status')[0].strip().split(',')

                list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "salesconsulting",
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


company_name = 'salesconsulting'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('salesconsulting',
                  'https://www.salesconsulting.ro/images/logo.png'
                  ))