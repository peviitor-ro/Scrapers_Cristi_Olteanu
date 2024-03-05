#
# Company - > Consensys
# Link -> https://consensys.io/open-roles?location=83558
#

from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():
    list_jobs = []

    req = requests.get("https://consensys.io/open-roles?location=83558", headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, "lxml")

    jobs = soup.find_all('div', class_='card-job svelte-11focjo')

    for job in jobs:
       link = 'https://consensys.io/' + job.find('a', class_='svelte-11focjo')['href']
       title = job.find('h5', class_='job-title svelte-11focjo').text
       location = job.find('div', class_='job-location svelte-11focjo').text

       if 'EMEA - Remote' in location:
           list_jobs.append({
               "job_title": title,
               "job_link": link,
               "company": "Consensys",
               "country": "Romania",
               "city": 'Cluj-Napoca',
               "remote": 'remote'
           })

    return list_jobs


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