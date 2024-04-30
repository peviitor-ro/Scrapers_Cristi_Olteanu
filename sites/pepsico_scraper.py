#
# Company - > Pepsico
# Link -> https://www.pepsicojobs.com/main/jobs?stretchUnits=MILES&stretch=10&location=Romania&lat=46&lng=25&woe=12&page=2&country=Romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():
    url = 'https://www.pepsicojobs.com/api/jobs?page=1&limit=100&country=Romania&sortBy=relevance&descending=false&internal=false'
    response = requests.get(url, headers=DEFAULT_HEADERS).json()['jobs']
    list_jobs = []

    for job in response:

        full_location = str(job['data']['full_location']).split(';')
        city = ''

        for loc in full_location:
            if 'Romania' in loc:
                city = validate_city(loc.strip().split(',')[0])

        list_jobs.append({
            "job_title": job['data']['title'],
            "job_link": job['data']['meta_data']['canonical_url'],
            "company": "Pepsico",
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


company_name = 'Pepsico'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Pepsico',
                  'https://cms.jibecdn.com/prod/pepsico-stg/assets/V2-HEADER-NAV_LOGO-en-us-1674467727089.svg'))

