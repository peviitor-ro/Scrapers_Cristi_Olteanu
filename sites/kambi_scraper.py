#
# Company - > Kambi
# Link -> https://boards.eu.greenhouse.io/kambi
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county


def get_jobs():

    list_jobs = []

    response = requests.get('https://boards-api.greenhouse.io/v1/boards/kambi/jobs', headers=DEFAULT_HEADERS)
    data = response.json()

    for job in data.get('jobs', []):
        location = job.get('location', {}).get('name', '')
        
        if 'Romania' in location or 'Bucharest' in location:
            title = job.get('title', '')
            link = job.get('absolute_url', '')
            
            if 'Remote' in location:
                remote_type = 'remote'
            elif 'Hybrid' in location:
                remote_type = 'hybrid'
            else:
                remote_type = 'on-site'
            
            city = location.split(',')[0].strip() if ',' in location else location.split()[0].strip()
            
            city_translations = {
                'Bucharest': 'București',
            }
            city = city_translations.get(city, city)
            
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Kambi",
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


company_name = 'Kambi'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Kambi',
                  'https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/043/510/resized/Kambi_Logo_2023.png?1673968948'
                  ))

