#
#  Company - > wyser
# Link -> https://ro.wyser-search.com/job-offers/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get(url='https://ro.wyser-search.com/job-offers/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('article', class_='px-0 col-12 col-sm-6 col-xl-4 py-3 card-job')

    for job in jobs:
        link = job.find('a',class_='dettaglio')['href']
        title = job.find('div', class_='col-10').text.strip()

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "wyser",
            "country": "Romania",
            "city": 'Bucuresti'
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'wyser'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('wyser',
                  'https://ro.mywyser.com/assets/images/logo-wyser.png'
                  ))