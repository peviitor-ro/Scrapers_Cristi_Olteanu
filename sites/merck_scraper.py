#
#  Company - > Merck
# Link -> https://careers.merckgroup.com/global/en/search-results
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import json
import urllib.parse
from _county import get_county
from _validate_city import validate_city


PHENOM_CDN = 'https://content-ir.phenompeople.com/api/MQAMKDGLOBAL/eagerLoadRefineSearch'


def get_jobs():
    list_jobs = []
    seen_ids = set()
    offset = 0
    page_size = 500

    while True:
        payload = json.dumps({'from': offset, 'size': page_size})
        url = f'{PHENOM_CDN}?locale=en_global&siteType=external&deviceType=desktop&payload={urllib.parse.quote(payload)}'

        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)

        if response.status_code != 200:
            break

        data = response.json()
        jobs_data = data.get('eagerLoadRefineSearch', data)
        jobs = jobs_data.get('data', {}).get('jobs', [])
        total = jobs_data.get('totalHits', 0)

        if not jobs:
            break

        for job in jobs:
            if job.get('country') != 'Romania':
                continue

            job_id = job.get('jobId', '')
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            title = job.get('title', '')
            city = validate_city(job.get('city', ''))
            link = f'https://careers.merckgroup.com/global/en/job/{job_id}'

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Merck",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": 'on-site'
            })

        offset += page_size
        if offset >= total:
            break

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Merck'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Merck',
                  'https://www.in.gr/wp-content/uploads/2021/03/merck-kgaa-vector-logo-150x83.png'
                  ))