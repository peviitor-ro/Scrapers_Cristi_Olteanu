#
#  Company - > grubhub
# Link -> https://grubhub.wd1.myworkdayjobs.com/External?locations=bd40add6f053101305ce49922a350000
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
import re

session = requests.Session()


def get_cookies() -> tuple:

    response = session.head(
        url='https://grubhub.wd1.myworkdayjobs.com/wday/cxs/grubhub/External/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    cf_id = re.search(r"__cf_bm=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response))
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, cf_id, wday_vps, wd_browser_id


def prepare_post():

    cookies = get_cookies()
    url = "https://grubhub.wd1.myworkdayjobs.com/wday/cxs/grubhub/External/jobs"
    payload = {
        "appliedFacets": {"locations": ["bd40add6f053101305ce49922a350000"]},
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
        "Origin": "https://grubhub.wd1.myworkdayjobs.com",
        "Referer": "https://grubhub.wd1.myworkdayjobs.com/External?locations=bd40add6f053101305ce49922a350000",
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

    jobs_list = []
    data = prepare_post()
    response = session.request("POST", data[0], json=data[1], headers=data[2]).json()['jobPostings']

    for job in response:
        jobs_list.append({
            "job_title": job['title'],
            "job_link": 'https://grubhub.wd1.myworkdayjobs.com/en-US/External'+job['externalPath'],
            "company": "grubhub",
            "country": "Romania",
            "city": job['locationsText'].split('-')[-1].replace('Cluj', 'Cluj-Napoca'),
        })
    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'grubhub'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('grubhub',
                  'https://grubhub.wd1.myworkdayjobs.com/wday/cxs/grubhub/External/sidebarimage/0bb5805e0316100db7c195c7df9a0000'
                  ))