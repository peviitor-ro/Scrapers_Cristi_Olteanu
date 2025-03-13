#
# Company - > salesconsulting
# Link ->https://salesconsulting.teamtailor.com/jobs?page=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county


def get_soup(url):

    session = requests.Session()
    response = session.get(url, headers=DEFAULT_HEADERS)
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
            text = job.find('a', class_='flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded')

            if text is not None:
                link = text['href']
                title = job.find('span', class_='text-block-base-link sm:min-w-[25%] sm:truncate company-link-style hyphens-auto')[
                    'title']
                info_text = job.find('div', class_='mt-1 text-md').text.split('·')[-1].strip().split()[-1]

                if 'remote' in info_text.lower():
                    job_type = 'remote'
                    city = job.find('div', class_='mt-1 text-md').text.split('·')[-2].strip()
                elif 'hybrid' in info_text.lower():
                    job_type = 'hybrid'
                    city = job.find('div', class_='mt-1 text-md').text.split('·')[-2].strip()
                else:
                    job_type = 'on-site'
                    city = info_text

                if 'locations' in city.lower():
                    soup_city = get_soup(link)
                    try:
                        city = soup_city.find('dl',
                                          class_='md:max-w-[70%] mx-auto text-md gap-y-0 md:gap-y-5 flex flex-wrap flex-col md:flex-row company-links'
                                          ).text.split('Locations')[1].split('Status')[0].strip().split('\n')[0].split(', ')
                    except:
                        city = soup_city.find('dl',
                                          class_='md:max-w-[70%] mx-auto text-md gap-y-0 md:gap-y-5 flex flex-wrap flex-col md:flex-row company-links'
                                          ).text.split('Locations')[1].strip().split('\n')[0].split(', ')

                try:
                    city = city.split(', ')
                except:
                    pass

                if 'Mureș' in city:
                    city = 'Targu-Mures'
                elif 'Turzii' in city:
                    city = 'Câmpia Turzii'
                elif 'Multiple locations' in city or 'Bucharest' in city:
                    city = 'Bucuresti'
                elif city == 'Mare':
                    city = 'Satu Mare'

                if city not in [['Chisinau'], ['Ruse']]:
                    list_jobs.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "salesconsulting",
                        "country": "Romania",
                        "city": city,
                        "county": get_county(city),
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
