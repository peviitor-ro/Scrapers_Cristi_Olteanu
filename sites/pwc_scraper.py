#
#  Company - > pwc
# Link -> https://jobs-cee.pwc.com/ce/en/search-results
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import re
import uuid

session = requests.Session()

def get_cookies() -> tuple:

    response = session.head(
        url='https://jobs-cee.pwc.com/widgets',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group(0)

    return play_session, phpppe_act


def prepare_post():

    cookies = get_cookies()

    url = "https://jobs-cee.pwc.com/widgets"

    payload = {
        "lang": "en_ce",
        "deviceType": "desktop",
        "country": "ce",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": ["category", "country", "city", "type", "managementLevel", "experienceLevel"],
        "size": 100,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page26",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": {"country": ["Romania"]},
        "locationData": {}
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{cookies[0]}{cookies[1]}",
        "Origin": "https://jobs-cee.pwc.com",
        "Referer": "https://jobs-cee.pwc.com/ce/en/search-results",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }

    return url, payload,headers


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = session.request("POST", data[0], json=data[1], headers=data[2]).json()['refineSearch']['data']['jobs']

    for job in response:
        title = job['title']
        city = job['city'].split()[0]
        link = f"https://jobs-cee.pwc.com/ce/en/job/{job['jobId']}"

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "pwc",
            "country": "Romania",
            "city": city,
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'pwc'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('pwc',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/PricewaterhouseCoopers_Logo.svg/790px-PricewaterhouseCoopers_Logo.svg.png'
                  ))