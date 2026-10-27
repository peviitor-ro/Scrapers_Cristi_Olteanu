#
#  Company - > hiveMq
# Link -> https://jobs.ashbyhq.com/hivemq
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
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

    list_jobs = []

    req = requests.get(
        "https://api.ashbyhq.com/posting-api/job-board/hivemq",
        headers=DEFAULT_HEADERS,
    )
    jobs = req.json().get('jobs', [])

    for job in jobs:
        if not job.get('isListed', True):
            continue

        location = (job.get('location') or '').strip()
        location_lower = location.lower()

        is_remote = bool(job.get('isRemote')) or location_lower.startswith('remote') or (job.get('workplaceType') or '').lower() == 'remote'
        if not is_remote:
            continue

        if any(region in location_lower for region in EXCLUDED_REGIONS):
            continue

        title = (job.get('title') or '').strip()
        link = job.get('jobUrl') or job.get('applyUrl')
        if not title or not link:
            continue

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "hiveMq",
            "country": "Romania",
            "city": 'Bucuresti',
            "county": 'Bucuresti',
            "remote": 'remote'
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'hiveMq'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hiveMq',
                  'https://www.hivemq.com/img/svg/hivemq-logo-vert.svg'
                  ))

