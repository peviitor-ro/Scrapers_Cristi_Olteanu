#
#  Company - > extia
# Link -> https://www.extia-group.com/fr-en/join-us?page=1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_link_id():
    response = requests.get('https://www.extia-group.com/fr-en/join-us?page=1',                         )
    soup = BeautifulSoup(response.text, 'lxml')
    link_id = str(soup.find_all('script', src=True)).split()[-1].split('/')[3]

    return link_id


def get_jobs():

    link_id = get_link_id()
    list_jobs = []
    response = requests.get(f'https://www.extia-group.com/_next/data/{link_id}/fr-en/join-us.json?page=1&locations=103',
                            headers=DEFAULT_HEADERS).json()['pageProps']['jobOffers']

    for job in response:
        title = job['attributes']['title']
        link = 'https://www.extia-group.com/fr-en/join-us/' + job['attributes']['slug']
        city = job['attributes']['location_cities']['data'][0]['attributes']['city']

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "extia",
            "country": "Romania",
            "city": city,
            "remote": 'on-site'
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'extia'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('extia',
                  'https://images.crunchbase.com/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1413980233/zi0an1tbowiahpdvsbua.png'
                  ))