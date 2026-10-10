#
#  Company - > fotc
# Link -> https://fotc.jobsoid.com/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from _validate_city import validate_city
from _county import get_county


def get_jobs():

    list_jobs = []
    response = requests.get('https://fotc.jobsoid.com/api/v1/jobs',
                            headers=DEFAULT_HEADERS)
    jobs = response.json()

    for job in jobs:
        location = job.get('location') or {}
        location_text = ' '.join(str(location.get(field, '') or '')
                                 for field in ('title', 'city', 'state', 'country'))

        if 'Romania' not in location_text:
            continue

        title = job.get('title')
        link = job.get('hostedUrl')
        city = validate_city(location.get('city') or location.get('title') or '')
        job_type = 'remote' if 'remote' in location_text.lower() else 'on-site'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "fotc",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": job_type
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'fotc'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('fotc',
                  'https://fotc.jobsoid.com/PortalJob/GetPortalLogo?size=medium'
                  ))
