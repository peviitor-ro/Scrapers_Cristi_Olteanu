# https://www.endava.com/careers/jobs?locations=Suceava/security-operations-center-soc-manager-msdrp-14451
# endava

from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import re
from _county import get_county
from _validate_city import validate_city


def get_cookies():

    response = requests.head(url='https://www.endava.com/jobs', headers=DEFAULT_HEADERS).headers
    cf_bm = re.search(r"__cf_bm=([^;]+);", str(response)).group(0)

    return cf_bm


def get_jobs():

    jobs_list = []
    cookie = get_cookies()
    url = "https://www.endava.com/_hcms/api/jobs"
    headers = {
        "cookie": f'{cookie}',
         "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    response = requests.post(url=url, headers=headers).json()['data']['HUBDB']

    jobs = response['jobs_en_collection']['items']
    locations = response['jobs_locations_collection']['items']
    all_romanian_cities = ['Brasov', 'Bucharest', 'Cluj-Napoca', 'Craiova', 'Iasi', 'Other Romanian Locations',
                           'Pitesti', 'Sibiu', 'Suceava', 'Targu Mures', 'Timisoara']

    filtered_cities = [city for city in locations if city['name'] in all_romanian_cities]

    for job in jobs:
        title = job['name']
        link = f"https://www.endava.com/careers/jobs/{job['hs_path']}"
        cities = job['locations_id'].split(',')
        romanian_cities = []
        job_type = 'on-site'

        for city in cities:
            for filtered_city in filtered_cities:
                if city == filtered_city['hs_id']:
                    romanian_cities.append(validate_city(filtered_city['name']))

        if 'Other Romanian Locations' in romanian_cities:
            romanian_cities.remove('Other Romanian Locations')
            job_type = 'remote'

        if romanian_cities:
            jobs_list.append({
                "job_title": title,
                "job_link": link,
                "company": "endava",
                "country": "Romania",
                "city": romanian_cities,
                "county": get_county(romanian_cities),
                "remote": job_type
            })
    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'endava'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('endava',
                  'https://companieslogo.com/img/orig/DAVA_BIG-e242e842.png?t=1632326300'
                  ))