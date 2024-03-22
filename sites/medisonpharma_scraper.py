#
# Company - > Medison
# Link -> https://www.medisonpharma.com/careers/?positions
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():
    list_jobs = []

    response = requests.get('https://www.medisonpharma.com/careers/?positions', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('a', class_='comeet-position')

    for job in jobs:
        link = job['href'].strip('//')
        if 'romania' in link:
            title = job.find('div', class_='comeet-position-name').text.strip()

            list_jobs.append({
                "job_title": title,
                "job_link": 'https:'+link,
                "company": "Medison",
                "country": "Romania",
                "city": 'Bucuresti',
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Medison'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Medison',
                  'https://mma.prnewswire.com/media/1527224/MEDISON_Logo.jpg?w=200'
                  ))


