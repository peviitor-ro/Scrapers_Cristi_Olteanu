#
#  Company - > extia
# Link -> https://www.extia-group.com/fr-en/join-us?page=1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import re
from _county import get_county


JOBS_URL = 'https://www.extia-group.com/fr-en/join-us?page=1'
BUCHAREST_LOCATION_ID = 'w9v9xjqtvecyzsw965sa9mlk'
CITY_TRANSLATIONS = {
    'Bucharest': 'Bucuresti'
}


def get_link_id():
    response = requests.get(JOBS_URL, headers=DEFAULT_HEADERS)
    match = re.search(r'/_next/static/([^/]+)/_buildManifest\.js', response.text)
    if match:
        return match.group(1)
    raise ValueError("Could not find Next.js build ID")


def get_jobs():

    link_id = get_link_id()
    list_jobs = []
    response = requests.get(
        f'https://www.extia-group.com/_next/data/{link_id}/fr-en/join-us.json?page=1&locations={BUCHAREST_LOCATION_ID}',
        headers=DEFAULT_HEADERS
    ).json()['pageProps']['jobOffers']

    for job in response:
        title = job['offer']['title'].strip()
        link = 'https://www.extia-group.com/fr-en/join-us/' + job['slug']
        city = CITY_TRANSLATIONS.get(job['offer']['location_city']['city'], job['offer']['location_city']['city'])

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "extia",
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


company_name = 'extia'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('extia',
                  'https://images.crunchbase.com/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1413980233/zi0an1tbowiahpdvsbua.png'
                  ))
