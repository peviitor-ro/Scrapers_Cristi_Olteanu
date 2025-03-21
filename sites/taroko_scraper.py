#
# Company - > taroko
# Link - https://taroko.breezy.hr/?&location=Romania#positions
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get('https://taroko.breezy.hr/?&location=Romania#positions', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')
    jobs = soup.find_all('li', class_='position transition')

    for job in jobs:

        link = 'https://taroko.breezy.hr' + job.find('a')['href']
        title = job.find('h2').text
        job_type = 'remote' if 'remote' in job.find('li', class_='location').text.lower() else 'on-site'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "taroko",
            "country": "Romania",
            "city": "Bucuresti",
            "county": "Bucuresti",
            "remote": job_type
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'taroko'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('taroko',
                  'https://gallery-cdn.breezy.hr/7f605790-c833-495e-9cda-b09c680881d9/taroko-logo.png'
                  ))