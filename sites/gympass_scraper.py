
#
#  Company - > Gympass (now Wellhub)
# Link -> https://boards.greenhouse.io/gympass
#
import requests
from bs4 import BeautifulSoup
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
from _county import get_county


def get_jobs():

    list_jobs = []

    response = requests.get('https://boards-api.greenhouse.io/v1/boards/gympass/jobs', headers=DEFAULT_HEADERS)
    data = response.json()

    for job in data.get('jobs', []):
        location = job.get('location', {}).get('name', '')
        
        if 'Romania' in location:
            title = job.get('title', '')
            link = job.get('absolute_url', '')
            
            if 'Remote' in location:
                remote_type = 'remote'
            elif 'Hybrid' in location:
                remote_type = 'hybrid'
            else:
                remote_type = 'on-site'
            
            location_part = location.split('(')[1].strip(')') if '(' in location else location
            city = location_part.split(' - ')[0].strip() if ' - ' in location_part else location.strip()
            if city == 'Romania':
                city = location.split('(')[0].strip()
            
            city_translations = {
                'Bucharest': 'București',
            }
            city = city_translations.get(city, city)
            
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Gympass",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": remote_type
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Gympass'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Gympass',
                  'https://s2-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/188/200/resized/Gympass_cover.png?1607553944'
                  ))