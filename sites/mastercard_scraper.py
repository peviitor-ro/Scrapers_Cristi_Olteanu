#
#  Company - > mastercard
# Link -> https://careers.mastercard.com/us/en/search-results?qcountry=Romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import json
import requests

BASE_URL = 'https://careers.mastercard.com'
WIDGETS_URL = f'{BASE_URL}/widgets'
PAGE_SIZE = 100

session = requests.Session()


def get_cookies() -> tuple:

    session.head(
        url=WIDGETS_URL,
        headers=DEFAULT_HEADERS,
        timeout=30)

    play_session = session.cookies.get('PLAY_SESSION')
    phpppe_act = session.cookies.get('PHPPPE_ACT')
    return (
        f'PLAY_SESSION={play_session};' if play_session else '',
        f'PHPPPE_ACT={phpppe_act};' if phpppe_act else ''
    )


def prepare_post(cookies, size=PAGE_SIZE, offset=0, selected_fields=None, keywords=''):

    payload = {
        "lang": "en_us",
        "deviceType": "desktop",
        "country": "us",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": offset,
        "jobs": True,
        "counts": True,
        "all_fields": ["category", "country", "state", "city", "postalCode", "jobType"],
        "size": size,
        "clearAll": selected_fields is None,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page11",
        "siteType": "external",
        "keywords": keywords,
        "global": True
    }
    if selected_fields is not None:
        payload["selected_fields"] = selected_fields

    headers = {
       "Accept": "application/json",
       "Accept-Language": "en-US",
       "Connection": "keep-alive",
       "Content-Type": "application/json",
       "Cookie": f"{cookies[0]}{cookies[1]}",
       "Origin": BASE_URL,
       "Referer": f"{BASE_URL}/us/en/search-results",
       "Sec-Fetch-Dest": "empty",
       "Sec-Fetch-Mode": "cors",
       "Sec-Fetch-Site": "same-origin",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
       "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
       "sec-ch-ua-mobile": "?0",
       "sec-ch-ua-platform": "Windows",
    }
    return WIDGETS_URL, payload, headers


def is_romania_job(job):

    values = [
        job.get('country'),
        job.get('cityStateCountry'),
        job.get('location'),
        job.get('address'),
        job.get('city'),
        job.get('state'),
        json.dumps(job.get('multi_location', ''), ensure_ascii=False),
        json.dumps(job.get('multi_location_array', ''), ensure_ascii=False)
    ]
    return any('romania' in str(value).lower() for value in values if value)


def fetch_jobs(cookies, selected_fields=None):

    offset = 0
    while True:
        url, payload, headers = prepare_post(cookies, offset=offset, selected_fields=selected_fields)
        response = session.post(url, json=payload, headers=headers, timeout=30).json()
        search = response.get('refineSearch', {})
        jobs = search.get('data', {}).get('jobs', [])
        total = search.get('totalHits') or search.get('hits') or 0

        yield from jobs

        offset += len(jobs)
        if not jobs or offset >= total:
            break


def get_jobs():

    list_jobs = []
    seen_jobs = set()
    cookies = get_cookies()

    jobs = list(fetch_jobs(cookies, {"country": ["Romania"]}))
    if not jobs:
        jobs = [job for job in fetch_jobs(cookies) if is_romania_job(job)]

    for job in jobs:
        job_id = job.get('jobId')
        title = job.get('title')

        if not job_id or not title or job_id in seen_jobs:
            continue

        seen_jobs.add(job_id)
        link = f'{BASE_URL}/us/en/job/{job_id}'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "mastercard",
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


company_name = 'mastercard'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mastercard',
                  'https://cdn.vox-cdn.com/thumbor/tFVfkB8D8iB_dOZ-lVnZHaX4_X0=/0x0:1000x1000/920x613/filters:focal(421x430:581x590)/cdn.vox-cdn.com/uploads/chorus_image/image/62800797/Mastercard_logo.0.jpg'
                  ))

