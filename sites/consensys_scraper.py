#
# Company - > Consensys
# Link -> https://jobs.ashbyhq.com/consensys
#

from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests


EXCLUDED_REGIONS = (
    'apac',
    'asia',
    'australia',
    'united states',
    'usa',
    'canada',
    'americas',
    'new york',
)


def get_jobs():
    jobs_list = []

    req = requests.get(
        "https://api.ashbyhq.com/posting-api/job-board/consensys",
        headers=DEFAULT_HEADERS,
    )
    jobs = req.json().get('jobs', [])

    for job in jobs:
        if not job.get('isListed', True):
            continue

        location = (job.get('location') or '').strip()
        location_lower = location.lower()

        is_remote = bool(job.get('isRemote')) or location_lower.startswith('remote')
        if not is_remote:
            continue

        if any(region in location_lower for region in EXCLUDED_REGIONS):
            continue

        title = (job.get('title') or '').strip()
        link = job.get('jobUrl') or job.get('applyUrl')
        if not title or not link:
            continue

        jobs_list.append({
            "job_title": title,
            "job_link": link,
            "company": "Consensys",
            "country": "Romania",
            "city": 'Bucuresti',
            "county": 'Bucuresti',
            "remote": 'remote'
        })
    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Consensys'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Consensys',
                  'https://consensys.io/_app/immutable/assets/logo.b5f12401.svg'
                  ))
