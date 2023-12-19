#
#  Company - > Milwaukee
# Link -> https://ttiemea.wd3.myworkdayjobs.com/ro-RO/TTI
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import uuid
import re

session = requests.Session()

def get_cookies() -> tuple:

    response = session.head(
        url='https://ttiemea.wd3.myworkdayjobs.com/wday/cxs/ttiemea/TTI/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, ts_id, wday_vps, wd_browser_id


def prepare_post():

    cookies = get_cookies()
    url = "https://ttiemea.wd3.myworkdayjobs.com/wday/cxs/ttiemea/TTI/jobs"
    payload = {
        "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{cookies[0]}{cookies[1]}{cookies[2]}{cookies[3]}",
        "Origin": "https://ttiemea.wd3.myworkdayjobs.com",
        "Referer": "https://ttiemea.wd3.myworkdayjobs.com/ro-RO/TTI?",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }
    return url,payload, headers


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = session.request("POST", data[0], json=data[1], headers=data[2]).json()['jobPostings']

    for job in response:
        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": job['title'],
            "job_link": 'https://ttiemea.wd3.myworkdayjobs.com/ro-RO/TTI'+job['externalPath'],
            "company": "Milwaukee",
            "country": "Romania",
            "city": 'Bucuresti',
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Milwaukee'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Milwaukee',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Milwaukee_Logo.svg/800px-Milwaukee_Logo.svg.png'
                  ))