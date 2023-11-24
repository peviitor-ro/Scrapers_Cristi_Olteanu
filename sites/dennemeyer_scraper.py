#
#  Company - > dennemeyer
# Link -> https://dennemeyer.wd3.myworkdayjobs.com/dennemeyer_careers?locations=99c9060b642e1001e86635de40a00000
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import re


def get_ids() -> tuple:
    response = requests.head(
        url='https://dennemeyer.wd3.myworkdayjobs.com/wday/cxs/dennemeyer/dennemeyer_careers/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, ts_id, wday_vps, wd_browser_id


def get_jobs():
    list_jobs = []

    data = get_ids()

    url = "https://dennemeyer.wd3.myworkdayjobs.com/wday/cxs/dennemeyer/dennemeyer_careers/jobs"

    payload = {
        "appliedFacets": {"locations": ["99c9060b642e1001e86635de40a00000","023dd96435d8016f98adf461d036dbdb"]},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{data[0]}{data[1]}{data[2]}{data[3]}",
        "Origin": "https://dennemeyer.wd3.myworkdayjobs.com",
        "Referer": "https://dennemeyer.wd3.myworkdayjobs.com/dennemeyer_careers?",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36.",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }

    response = requests.post(url=url, json=payload, headers=headers).json()['jobPostings']

    for job in response:
        title = job['title']
        link = 'https://dennemeyer.wd3.myworkdayjobs.com/en-US/dennemeyer_careers' + job['externalPath']

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "dennemeyer",
            "country": "Romania",
            "city": 'Brasov'
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'dennemeyer'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('dennemeyer',
                  'https://image4.owler.com/logo/dennemeyer_owler_20171101_143412_large.jpg'
                  ))