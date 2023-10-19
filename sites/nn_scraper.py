
#
#  Company - > NN
# Link -> https://nngroup.wd3.myworkdayjobs.com/en-US/WDExternal?locationCountry=f2e609fe92974a55a05fc1cdc2852122
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import uuid
import re

session = requests.Session()

def get_ids() -> tuple:

    response = session.head(
        url='https://nngroup.wd3.myworkdayjobs.com/wday/cxs/nngroup/WDExternal/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session,ts_id, wday_vps, wd_browser_id

def prepare_post():

    cookies = get_ids()

    url = "https://nngroup.wd3.myworkdayjobs.com/wday/cxs/nngroup/WDExternal/jobs"

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
        "Origin": "https://nngroup.wd3.myworkdayjobs.com",
        "Referer": "https://nngroup.wd3.myworkdayjobs.com/en-US/WDExternal",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }
    return url, headers, payload


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = session.request("POST", data[0], json=data[2], headers=data[1]).json()['jobPostings']

    for job in response:
        title = job['title']
        link = 'https://nngroup.wd3.myworkdayjobs.com/en-US/WDExternal'+job['externalPath']
        city = job['locationsText']

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "NN",
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


company_name = 'NN'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('NN',
                  'https://companieslogo.com/img/orig/NN.AS_BIG-73c1d014.png?t=1656142642'
                  ))





