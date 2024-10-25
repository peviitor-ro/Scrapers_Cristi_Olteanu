#
# Company - > nVent
# Link -> https://nvent.wd5.myworkdayjobs.com/en-US/nVent/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import re
from _validate_city import validate_city
from _county import get_county

session = requests.Session()


def get_ids() -> tuple:

    response = session.head(
        url='https://nvent.wd5.myworkdayjobs.com/en-US/nVent?locations=090e2b79c4a401eecfe42da8fb10ca48&locations=8ed57ec2277e01cfca042a6a9c01c50e',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    csrf_token = re.search(r"CALYPSO_CSRF_TOKEN=([^;]+);", str(response)).group(0)
    cf_id = re.search(r"__cf_bm=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, csrf_token, cf_id, wday_vps, wd_browser_id


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
            "locations": ["8ed57ec2277e01cfca042a6a9c01c50e","9977415ffa0a012794621c8e47135f31","090e2b79c4a401247bb7e70bbf105717","090e2b79c4a401eecfe42da8fb10ca48"]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    return url, headers, data


def get_job_type(url):
    try:
        job_type = requests.get(url, headers=DEFAULT_HEADERS).json()['jobPostingInfo']['remoteType']
    except:
        job_type = 'on-site'
    return job_type


def get_city(url):
    response = requests.get(url, headers=DEFAULT_HEADERS).json()['jobPostingInfo']
    city = response['location'].split(',')[0]
    romanian_city = ['Ploiesti', 'Brasov', 'Prejmer']
    additional_cities = response.get('additionalLocations')

    if city not in romanian_city:
        if additional_cities:
            for additional_city in additional_cities:
                if additional_city in romanian_city:
                    city = additional_city
    return city


def get_jobs():

    url, headers, data = prepare_post()
    response = session.post(url=url, headers=headers, json=data).json()

    list_jobs = []
    for job in response['jobPostings']:
        link_request = 'https://nvent.wd5.myworkdayjobs.com/wday/cxs/nvent/nVent' + job['externalPath']
        job_type = get_job_type(link_request)
        city = get_city(link_request)

        list_jobs.append({
            "job_title": job['title'],
            "job_link": 'https://nvent.wd5.myworkdayjobs.com/en-US/nVent' + job['externalPath'],
            "company": "nVent",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": job_type
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