
#
#  Company - > Levis
# Link -> https://levistraussandco.wd5.myworkdayjobs.com/ro-RO/External/?q=Romania
#
import requests
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import re
from _county import get_county
from _validate_city import validate_city

session = requests.Session()


def get_ids() -> tuple:

    response = session.head(
        url='https://levistraussandco.wd5.myworkdayjobs.com/ro-RO/External/?q=Romania',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    csrf_token = re.search(r"CALYPSO_CSRF_TOKEN=([^;]+);", str(response)).group(0)
    cf_id = re.search(r"__cf_bm=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, csrf_token, cf_id, wday_vps, wd_browser_id


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


def get_city(url):

    response_ = requests.get(url, headers=DEFAULT_HEADERS).json()['jobPostingInfo']
    additional_locations = response_['additionalLocations']

    for additional_location in additional_locations:
        if 'Romania' in additional_location:
            city = additional_location.split(',')[0]
    return city


def get_jobs():

    jobs_list = []
    url, headers, data = prepare_post()
    response = session.post(url=url, headers=headers, json=data).json()

    for job in response['jobPostings']:

        country = job['bulletFields'][2].split(',')[-1]
        link_request = ('https://levistraussandco.wd5.myworkdayjobs.com/wday/cxs/levistraussandco/External'
                        + job['externalPath'])

        if 'Romania' in country:
            city = job['bulletFields'][2].split(',')[0]
        else:
            city = get_city(link_request)
        city = validate_city(city)

        jobs_list.append({
            "job_title": job['title'],
            "job_link": 'https://levistraussandco.wd5.myworkdayjobs.com/ro-RO/External'+job['externalPath'],
            "company": "Levis",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": 'on-site'
        })
    return jobs_list


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
                  'https://www.kindpng.com/picc/m/83-838136_levis-logo-levis-logo-hd-png-download.png'
                  ))

