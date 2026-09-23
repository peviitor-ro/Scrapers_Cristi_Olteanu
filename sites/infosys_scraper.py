#
#  Company - > Infosys
# Link -> https://digitalcareers.infosys.com/infosys/global-careers?page=2&per_page=25&job_type=experienced&location=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import json
import requests
import urllib.parse
from _county import get_county
from _validate_city import validate_city


ALGOLIA_APP_ID = 'UM59DWRPA1'
ALGOLIA_API_KEY = 'c8bffc42453b5122fd7e0aeb42761027'
ALGOLIA_INDEX = 'production_Infosys_jobs'
ALGOLIA_URL = f'https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/{ALGOLIA_INDEX}/query'


def search_jobs(page: int = 0, per_page: int = 25):
    """
    Search Romania jobs on the Infosys Algolia index.
    """

    params = urllib.parse.urlencode({
        'filters': 'country:Romania',
        'hitsPerPage': per_page,
        'page': page,
    })

    headers = {
        **DEFAULT_HEADERS,
        'X-Algolia-Application-Id': ALGOLIA_APP_ID,
        'X-Algolia-API-Key': ALGOLIA_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.post(ALGOLIA_URL, headers=headers, data=json.dumps({'params': params}))
    response.raise_for_status()

    return response.json()


def get_pages():

    result = search_jobs()
    num_jobs = result.get('nbHits', 0)
    pages = int(num_jobs / 25)

    if num_jobs % 25 > 0:
        pages += 1
    else:
        pass

    return pages


def get_jobs():

    list_jobs = []

    for page in range(0, get_pages(), 1):
        result = search_jobs(page=page)
        jobs = result.get('hits', [])

        for job in jobs:
            redirects = job.get('redirect_url') or []
            link = redirects[0] if redirects else ''
            title = job.get('title', '')
            locations = job.get('work_location') or []

            if not locations:
                continue

            city = validate_city(locations[0].strip())

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Infosys",
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

company_name = 'Infosys'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Infosys',
                  'https://w7.pngwing.com/pngs/563/912/png-transparent-infosys-technologies-hd-logo-thumbnail.png'
                  ))