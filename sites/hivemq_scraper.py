#
#  Company - > hiveMq
# Link -> https://boards.eu.greenhouse.io/hivemq
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get('https://job-boards.eu.greenhouse.io/hivemq?t=f4020b82teu&offices%5B%5D=4000101101',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_='job-posts')

    for job in jobs:
        title = job.find('p', class_="body body--medium").text
        link = job.find('a')['href']
        location = job.find('p', class_='body body__secondary body--metadata').text

        if 'europe remote' in location.lower():
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "hiveMq",
                "country": "Romania",
                "city": 'Bucuresti',
                "county": 'Bucuresti',
                "remote": 'remote'
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'hiveMq'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hiveMq',
                  'https://www.hivemq.com/img/svg/hivemq-logo-vert.svg'
                  ))

