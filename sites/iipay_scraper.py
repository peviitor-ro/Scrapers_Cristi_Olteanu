#
# Company - > iiPay
# Link -> https://careers.vistra.com/  (iiPay is part of Vistra, the old
#         https://www.iipay.com/careers/ page no longer exists)
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city


SEARCH_URL = 'https://careers.vistra.com/services/recruiting/v1/jobs'
JOB_URL = 'https://careers.vistra.com/job/{title}/{job_id}-en_US/'


def get_jobs():

    list_jobs = []
    seen_ids = set()
    page_number = 0

    while True:
        payload = {
            "keywords": "iiPay",
            "locale": "en_US",
            "location": "Romania",
            "pageNumber": page_number,
            "sortBy": "recent",
        }

        response = requests.post(SEARCH_URL, json=payload, headers=DEFAULT_HEADERS)
        response.raise_for_status()
        jobs = response.json().get('jobSearchResult', [])

        if not jobs:
            break

        new_jobs = 0

        for item in jobs:
            job = item.get('response', {})
            job_id = str(job.get('id', ''))
            locations = ' '.join(job.get('jobLocationShort') or [])

            if not job_id or job_id in seen_ids or 'Romania' not in locations:
                continue

            seen_ids.add(job_id)
            new_jobs += 1
            title = job.get('unifiedStandardTitle') or job.get('urlTitle')
            url_title = job.get('urlTitle') or job.get('unifiedUrlTitle')
            city = validate_city('Romania')

            list_jobs.append({
                "job_title": title,
                "job_link": JOB_URL.format(title=url_title, job_id=job_id),
                "company": "iiPay",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": "remote"
            })

        if new_jobs == 0:
            break

        page_number += 1

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'iiPay'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('iiPay',
                  'https://www.iipay.com/wp-content/themes/theme_iipay/images/iiPay-Logo-Final-No-Tagline.svg'
                  ))
