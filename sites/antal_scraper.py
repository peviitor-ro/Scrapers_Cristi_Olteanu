#
#  Company - > Antal
# Link -> https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county
from _validate_city import validate_city


def get_soup(url):

    session = requests.Session()
    response = session.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_nr_pages():

    soup_pages = get_soup('https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page=')
    next_page = soup_pages.find('a', class_='next page-numbers')
    if next_page:
        nr_pages = int(next_page['href'].split('=')[-1])
    else:
        nr_pages = 1
    return nr_pages


def get_jobs():

    list_jobs = []

    for page in range(1, get_nr_pages() + 1, 1):

        soup_jobs = get_soup(f'https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page={page}')
        jobs = soup_jobs.find_all('li', class_='job-card')

        for job in jobs:
            title_elem = job.find('div', class_='job-card__title')
            if title_elem:
                title_link = title_elem.find('a')
                if title_link:
                    title = title_link.text.strip()
                    job_link = title_link['href']
                else:
                    continue
            else:
                continue

            try:
                details = job.find('ul', class_='job-card__details')
                city = ''
                if details:
                    lis = details.find_all('li')
                    if len(lis) >= 2:
                        city_line = lis[-1].text.strip()
                        if ',' in city_line:
                            city = city_line.split(',')[0].strip()
                        elif city_line.lower() != 'romania':
                            city = city_line.strip()
                    elif len(lis) == 1:
                        city_line = lis[0].text.strip()
                        if ',' in city_line:
                            city = city_line.split(',')[0].strip()
                        elif city_line.lower() != 'romania':
                            city = city_line.strip()
            except:
                city = ''

            city = validate_city(city)

            if 'on site' in title.lower() or 'on-site' in title.lower():
                job_type = 'on-site'
            elif 'hybrid' in title.lower() or 'hibrid' in title.lower():
                job_type = 'hybrid'
            elif 'remote' in title.lower() or 'ful-remote' in title.lower():
                job_type = 'remote'
            else:
                job_type = 'on-site'

            list_jobs.append({
                "job_title": title,
                "job_link": job_link,
                "company": "Antal",
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


company_name = 'Antal'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Antal',
                  'https://www.antal.com/app/public/images/logo.png'
                  ))
