#
# Company - > Adecco
# Link -> https://www.adecco.ro/jobs/?page=0
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county
from _validate_city import validate_city


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

            if 'remote' in city.lower() or 'remote' in title.lower() or 'Romania' in city:
                city = 'Bucuresti'
                job_type = 'remote'
            else:
                job_type = 'on-site'

            if 'Com' in city:
                city = city.split()[0]
            elif 'Bucuresti' in city or '104H' in city or 'Bucharest' in city:
                city = 'Bucuresti'
            elif 'Mures' in city or 'Tirgu' in city or 'Tîrgu Mureş' in city:
                city = 'Targu-Mures'
            elif 'stefanesti' in city.lower():
                city = 'Stefanestii de Jos'
            elif 'Satu' in city:
                city = 'Satu Mare'
            elif 'cluj' in city.lower():
                city = 'Cluj-Napoca'
            elif 'bolintin' in city.lower():
                city = 'Bolintin-Deal'
            elif 'ilfov' in city.lower():
                city = 'Buftea'
            elif 'ialomita' in city.lower():
                city = 'Slobozia'
            elif 'prahova' in city.lower():
                city = 'Ploiesti'
            elif 'otopeni' in city.lower():
                city = 'Otopeni'
            elif 'bacau/onesti' in city.lower():
                city = 'Onesti'
            elif 'berceni' in city.lower():
                city = 'Bucuresti'
            elif 'Mioveni - Pitesti' in city.strip():
                city = city.split(' - ')
            elif 'bihor' in city.lower():
                city = 'Oradea'

            city = validate_city(city)

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Adecco",
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

company_name = 'Adecco'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Adecco',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Adecco_logo.png/600px-Adecco_logo.png'
                  ))