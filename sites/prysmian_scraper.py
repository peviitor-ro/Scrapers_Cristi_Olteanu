#
# Company - > Prysmian
# Link -> https://prysmiangroup.wd3.myworkdayjobs.com/Careers?locationCountry=f2e609fe92974a55a05fc1cdc2852122
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import re
import requests
import uuid

session = requests.Session()


def get_cookies() -> tuple:

    response = session.head(
        url='https://prysmiangroup.wd3.myworkdayjobs.com/wday/cxs/prysmiangroup/Careers/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, ts_id, wday_vps, wd_browser_id


def prepare_post():

    cookies = get_cookies()

    url = "https://prysmiangroup.wd3.myworkdayjobs.com/wday/cxs/prysmiangroup/Careers/jobs"

    payload = {
        "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
        "searchText": ""
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{cookies[0]}{cookies[1]}{cookies[2]}{cookies[3]}",
        "Origin": "https://prysmiangroup.wd3.myworkdayjobs.com",
        "Referer": "https://prysmiangroup.wd3.myworkdayjobs.com/Careers",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }
    return url, payload, headers


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = requests.request("POST", data[0], json=data[1], headers=data[2]).json()['jobPostings']

    for job in response:
        title = job['title']
        link = 'https://prysmiangroup.wd3.myworkdayjobs.com/en-US/Careers' + job['externalPath']

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Prysmian",
            "country": "Romania",
            "city": 'Slatina',
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Prysmian'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Prysmian',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Prysmian_Group_Logo.png/800px-Prysmian_Group_Logo.png'
                  ))
