#
# Company - > Consensys
# Link -> https://consensys.io/open-roles?location=83558
#

from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():
    jobs_list = []

    req = requests.get("https://consensys.io/open-roles?location=83558", headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, "lxml")
    jobs = soup.find_all('a', class_='card-job svelte-rgojh5')

    for job in jobs:
       link = 'https://consensys.io/' + job.get('href')
       title = job.find('h5').text
       location = job.find('div', class_='job-location svelte-rgojh5').text

       if 'EMEA - Remote' in location or 'GLOBAL - Remote' in location:
           jobs_list.append({
               "job_title": title,
               "job_link": link,
               "company": "Consensys",
               "country": "Romania",
               "city": 'Cluj-Napoca',
               "county": 'Cluj',
               "remote": 'remote'
           })
    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Consensys'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Consensys',
                  'https://consensys.io/_app/immutable/assets/logo.b5f12401.svg'
                  ))