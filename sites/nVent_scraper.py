#
# Company - > nVent
# Link -> https://nvent.wd5.myworkdayjobs.com/en-US/nVent/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import uuid
import re

session = requests.Session()

def get_ids() -> tuple:

    response = session.head(
        url='https://nvent.wd5.myworkdayjobs.com/en-US/nVent?locations=090e2b79c4a401eecfe42da8fb10ca48&locations=8ed57ec2277e01cfca042a6a9c01c50e',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    csrf_token = re.search(r"CALYPSO_CSRF_TOKEN=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, csrf_token, ts_id, wday_vps, wd_browser_id

def prepare_post() -> tuple:

    play_session, csrf_token, ts_id, wday_vps, wd_browser_id = get_ids()

    url = 'https://nvent.wd5.myworkdayjobs.com/wday/cxs/nvent/nVent/jobs'

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': f'{wday_vps} timezoneOffset=-180; {play_session} {ts_id} {wd_browser_id} {csrf_token[:-1]}',
        'Origin': 'https://nvent.wd5.myworkdayjobs.com',
        'Referer': 'https://nvent.wd5.myworkdayjobs.com/en-US/nVent?locations=090e2b79c4a401eecfe42da8fb10ca48&locations=8ed57ec2277e01cfca042a6a9c01c50e',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-CALYPSO-CSRF-TOKEN': f'{csrf_token.split("=")[1]}'
    }

    data = {
        "appliedFacets": {
            "locations": ["090e2b79c4a401eecfe42da8fb10ca48", "8ed57ec2277e01cfca042a6a9c01c50e"]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    return url, headers, data

def get_jobs():

    url, headers, data = prepare_post()
    response = session.post(url=url, headers=headers, json=data).json()

    list_jobs = []
    for job in response['jobPostings']:
        city = job['locationsText'].split(',')[0].strip()
        if 'Locations' in city:
            city = 'Brasov'

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": job['title'],
            "job_link": 'https://nvent.wd5.myworkdayjobs.com/en-US/nVent' + job['externalPath'],
            "company": "nVent",
            "country": "Romania",
            "city": city
        })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'nVent'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('nVent',
                  'https://seeklogo.com/images/N/nvent-logo-E3845C5AC6-seeklogo.com.png'
                  ))