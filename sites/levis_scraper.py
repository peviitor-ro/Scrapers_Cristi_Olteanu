
#
#  Company - > Levis
# Link -> https://levistraussandco.wd5.myworkdayjobs.com/ro-RO/External/?q=Romania
#
import requests
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import uuid
import re

session = requests.Session()

def get_ids() -> tuple:

    response = session.head(
        url='https://levistraussandco.wd5.myworkdayjobs.com/wday/cxs/levistraussandco/External/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    csrf_token = re.search(r"CALYPSO_CSRF_TOKEN=([^;]+);", str(response))
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, csrf_token, ts_id, wday_vps, wd_browser_id

def prepare_post() -> tuple:
    play_session, csrf_token, ts_id, wday_vps, wd_browser_id = get_ids()

    url = 'https://levistraussandco.wd5.myworkdayjobs.com/wday/cxs/levistraussandco/External/jobs'

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': f'{wday_vps} timezoneOffset=-180; {play_session} {ts_id} {wd_browser_id} {csrf_token}',
        'Origin': 'https://levistraussandco.wd5.myworkdayjobs.com',
        'Referer': 'https://levistraussandco.wd5.myworkdayjobs.com/ro-RO/External/?Location_Country=f2e609fe92974a55a05fc1cdc2852122',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-CALYPSO-CSRF-TOKEN': f'{csrf_token}'
    }

    data = {
        "appliedFacets": {
            "Location_Country": ["f2e609fe92974a55a05fc1cdc2852122"]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    return url, headers, data


def get_jobs():
    url, headers, data = prepare_post()
    response = session.post(url=url, headers=headers, json=data).json()

    lst_with_data = []
    for job in response['jobPostings']:

        city = job['bulletFields'][2].split(',')[0]
        if city != 'Bucharest':
            city = 'Bucharest'

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": job['title'],
            "job_link": 'https://levistraussandco.wd5.myworkdayjobs.com/ro-RO/External'+job['externalPath'],
            "company": "Levis",
            "country": "Romania",
            "city": city
        })

    return lst_with_data

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'Levis'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Levis',
                  'https://e7.pngegg.com/pngimages/6/505/png-clipart-levi-strauss-co-clothing-jeans-company-denim-jeans-love-text-thumbnail.png'
                  ))

