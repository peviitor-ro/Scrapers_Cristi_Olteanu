#
# Company - > assaabloy
# Link -> https://www.assaabloy.com/career/en/open-positions
#

from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests


def get_jobs():

    res = requests.get(
        'https://integration-hub-prod-assets.globalweb.aws.assaabloy.com/job-openings/jobs.json',
        headers=DEFAULT_HEADERS, timeout=30)
    res.raise_for_status()

    list_jobs = []

    for job in res.json().get('items', []):
        locations = job.get('locations') or []
        if not any(location.get('country') == 'Romania' for location in locations):
            continue

        list_jobs.append({
            "job_title": job['title'],
            "job_link": 'https://www.assaabloy.com/career/en/open-positions/job.' + job['jobReqId'],
            "company": "assaabloy",
            "country": "Romania",
            "city": 'Bucuresti',
            "county": 'Bucuresti',
            "remote": 'on-site'
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'assaabloy'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('assaabloy',
                  'https://www.hpd-collaborative.org/wp-content/uploads/2019/07/ASSA-ABLOY-logo-300x200.jpg'
                  ))


