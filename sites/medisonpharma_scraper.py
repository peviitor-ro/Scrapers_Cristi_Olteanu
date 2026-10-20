#
# Company - > Medison
# Link -> https://www.medisonpharma.com/careers/?positions
#
# The careers page at medisonpharma.com is protected by Cloudflare and the
# positions are rendered client-side from the Comeet ATS. We query the Comeet
# Careers API directly instead, using the company UID/token published on the
# Comeet-hosted careers page (https://www.comeet.com/jobs/medison/67.00A).
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from _county import get_county
from _validate_city import validate_city
import requests

COMEET_COMPANY_UID = '67.00A'
COMEET_TOKEN = '76A2C7C163E33E625122C7C1DA8ED476A33E6'
COMEET_API = (
    f'https://www.comeet.co/careers-api/2.0/company/'
    f'{COMEET_COMPANY_UID}/positions?token={COMEET_TOKEN}&details=true'
)


def get_jobs():
    list_jobs = []

    response = requests.get(COMEET_API, headers=DEFAULT_HEADERS, timeout=30)
    positions = response.json()

    for position in positions:
        location = position.get('location', {})
        if location.get('country') != 'RO':
            continue

        job_link = (position.get('url_recruit_hosted_page')
                    or position.get('url_comeet_hosted_page')
                    or position.get('url_active_page'))
        if not job_link:
            continue

        city = validate_city(location.get('city') or '')
        county = location.get('state') or get_county(city)

        list_jobs.append({
            "job_title": position.get('name', '').strip(),
            "job_link": job_link,
            "company": "Medison",
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": 'on-site'
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
