#
#  Company - > bayware
# Link -> https://jobs.baywa-re.com/job-offers.html
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county


def get_soup(url):
    session = requests.Session()
    response = session.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():

    soup_pages = get_soup('https://jobs.baywa-re.com/job-offers.html?start=')
    pages = int(soup_pages.find('div', attrs={'id': 'countjobs'}).text)
    return pages


def get_jobs():

    list_jobs = []

    for page in range(0, get_pages(), 60):

        soup_jobs = get_soup(f'https://jobs.baywa-re.com/job-offers.html?start={page}')
        jobs = soup_jobs.find_all('tr')

        for job in jobs:
            text = job.find('td', class_='real_table_col1')
            if text is not None:
                link = text.find('a')['href']
                title = text.find('a').text
                country = job.find('td', class_='real_table_col5').text
                city = job.find('td', class_='real_table_col4').text.split(', ')

                if 'Romania' in country:
                    list_jobs.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "bayware",
                        "country": "Romania",
                        "city": city,
                        "county": get_county(city),
                        "remote": 'on-site'
                    })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'bayware'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('bayware',
                  'https://jobs.baywa-re.com/templates/bayware/images/Firmenlogo.png'
                  ))