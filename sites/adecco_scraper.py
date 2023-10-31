#
# Company - > Adecco
# Link -> https://www.adecco.ro/jobs/?page=0
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid


def get_soup(url: str):

    response = requests.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')
    return soup


def get_nr_pages():

    soup_nr = get_soup('https://www.adecco.ro/jobs/?page=0')
    nr_jobs = int(soup_nr.find('h1', class_='h6').text.split()[0])
    pages = int(nr_jobs/10)
    last_page = nr_jobs/10
    if last_page > 0:
        nr_pages = pages+1
    else:
        nr_pages = pages
    return nr_pages


def get_jobs():
    list_jobs = []

    for page in range(1, get_nr_pages()+1, 1):

        soup_jobs = get_soup(url='https://www.adecco.ro/jobs/?page=' + str(page))
        jobs = soup_jobs.find_all('div', class_='card no-side-padding-m')

        for job in jobs:
            city = job.find('ul', class_='list-unstyled').find('li').text.split(',')[0].strip()
            link = 'https://www.adecco.ro/jobs/'+job.find('a')['href']
            title = job.find('a').text

            if 'remote' in city.lower() or 'remote' in title.lower():
                city = ''
                job_type = 'remote'
            else:
                job_type = 'on-site'

            if 'Com' in city:
                city = city.split()[0]
            elif 'Bucuresti' in city or '104H' in city:
                city = 'Bucuresti'
            elif 'Mures' in city:
                city = 'Targu Mures'
            elif 'stefanestii' in city.lower():
                city = 'Stefanesti de Jos'

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Adecco",
                "country": "Romania",
                "city": city,
                "remote": job_type
            })

    return list_jobs

get_jobs()

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Adecco'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Adecco',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Adecco_logo.png/600px-Adecco_logo.png'
                  ))