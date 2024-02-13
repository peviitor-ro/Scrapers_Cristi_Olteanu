#
# Company - > Edenred
# Link -> https://www.edenred.ro/ro/descopera-jobul-potrivit
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_soup(url):

    r = requests.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_pages():
    response = requests.get('https://www.edenred.ro/ro/api/jobs?page=0&_=1696064805636', headers=DEFAULT_HEADERS).json()
    nr_pages = response['pager']['total_pages']

    return nr_pages


def get_jobs():

    list_jobs = []

    for page in range(0, get_pages()):
        res = requests.get(f'https://www.edenred.ro/ro/api/jobs?page={page}&_=1696064805636').json()['rows']

        for job in res:
            link = 'https://www.edenred.ro' + job['nid']
            cities = [job['field_locatie_job']]

            try:
                other_cities = get_soup(link).find_all('div', class_='widget'
                                                       )[1].find('p').find('span').text.split('or ')[-1].split('/')
                if 'Gheorghe' in other_cities or 'Brasov' in other_cities or 'Bucuresti' in other_cities:
                    cities.extend(other_cities)
            except:
                pass

            for i in range(len(cities)):
                if 'Gheorghe' in cities[i]:
                    cities[i] = 'Sfantu Gheorghe'

            list_jobs.append({
                "job_title": job['title'],
                "job_link": link,
                "company": "Edenred",
                "country": "Romania",
                "city": cities,
                "remote": 'hibrid'
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Edenred'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Edenred',
                  'https://www.edenred.ro/themes/custom/edenred/images/logo_25.svg'
                  ))