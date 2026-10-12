#
# Company - > Wiley
# Link - https://wiley.wd1.myworkdayjobs.com/en-US/wiley_careers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
import requests
from L_00_logo import update_logo
from _county import get_county


WORKDAY_BASE = "https://wiley.wd1.myworkdayjobs.com"
WORKDAY_TENANT = "wiley"
WORKDAY_SITE = "wiley_careers"
ROMANIA_COUNTRY_FACET = "f2e609fe92974a55a05fc1cdc2852122"


def _get_remote_type(external_path):

    url = f"{WORKDAY_BASE}/wday/cxs/{WORKDAY_TENANT}/{WORKDAY_SITE}{external_path}"
    headers = dict(DEFAULT_HEADERS)
    headers['Accept'] = 'application/json'

    try:
        response = requests.get(url=url, headers=headers, timeout=30).json()
    except (requests.RequestException, ValueError):
        return 'on-site'

    remote_type = str(response.get('jobPostingInfo', {}).get('remoteType') or '').lower()
    if 'hybrid' in remote_type:
        return 'hybrid'
    if 'remote' in remote_type:
        return 'remote'
    return 'on-site'


def get_jobs():

    list_jobs = []
    url = f"{WORKDAY_BASE}/wday/cxs/{WORKDAY_TENANT}/{WORKDAY_SITE}/jobs"
    headers = dict(DEFAULT_HEADERS)
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'

    offset = 0
    while True:
        payload = {
            "appliedFacets": {"locationCountry": [ROMANIA_COUNTRY_FACET]},
            "limit": 20,
            "offset": offset,
            "searchText": ""
        }
        response = requests.post(url=url, json=payload, headers=headers, timeout=30).json()
        jobs = response.get('jobPostings', [])
        if not jobs:
            break

        for job in jobs:
            location = job.get('locationsText', '')
            city = location.split(',')[0].strip() if ',' in location else location.strip()

            list_jobs.append({
                "job_title": job['title'],
                "job_link": f"{WORKDAY_BASE}/en-US/{WORKDAY_SITE}{job['externalPath']}",
                "company": "Wiley",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": _get_remote_type(job['externalPath'])
            })

        offset += 20
        if offset >= response.get('total', 0):
            break

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'Wiley'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Wiley',
                  'https://careers.wiley.com/img/logos/wiley-logo-black.svg'
                  ))
