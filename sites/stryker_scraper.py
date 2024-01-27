#
# Company - > stryker
# Link -> https://stryker.wd1.myworkdayjobs.com/StrykerCareers?Location_Country=f2e609fe92974a55a05fc1cdc2852122
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import re


def get_cookies() -> tuple:
    response = requests.head(
        url='https://stryker.wd1.myworkdayjobs.com/wday/cxs/stryker/StrykerCareers/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response))
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)
    cf_bm = re.search(r"__cf_bm=([^;]+);", str(response))
    cflb = re.search(r"__cflb=([^;]+);", str(response))

    return play_session, wday_vps, wd_browser_id, cflb, cf_bm


def prepare_post():

    cookies = get_cookies()
    url = 'https://stryker.wd1.myworkdayjobs.com/wday/cxs/stryker/StrykerCareers/jobs'
    payload = {
        "appliedFacets": {"Location_Country": ["f2e609fe92974a55a05fc1cdc2852122"]},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    headers = {
        "cookie": f"{cookies[0]}{cookies[1]}{cookies[2]}{cookies[3]}{cookies[4]}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    return url, payload, headers


def get_info(url):

    res = requests.get(url).json()['jobPostingInfo']['jobDescription']
    job_type_info = res.split(':')[1].split('<p')[0].strip()

    if 'hybrid' in job_type_info.lower():
        job_type = 'hibrid'
    elif 'remote' in job_type_info.lower():
        job_type = 'remote'
    else:
        job_type = 'onsite'

    return job_type


def get_jobs():

    jobs_list = []
    data = prepare_post()

    response = requests.post(url=data[0], json=data[1], headers=data[2]).json()['jobPostings']

    for job in response:
        link = 'https://stryker.wd1.myworkdayjobs.com/en-US/StrykerCareers' + job['externalPath']
        title = job['title']
        link_job_info = 'https://stryker.wd1.myworkdayjobs.com/wday/cxs/stryker/StrykerCareers' + job['externalPath']
        job_type = get_info(link_job_info)

        jobs_list.append({
            "job_title": title,
            "job_link": link,
            "company": "stryker",
            "country": "Romania",
            "city": 'Bucuresti',
            "remote": job_type
        })

    return jobs_list

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'stryker'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('stryker',
                  'https://stryker.wd1.myworkdayjobs.com/wday/cxs/stryker/StrykerCareers/sidebarimage/7bed2480eb810113b6d12edd2602fe00'
                  ))