#
# Company - > Microchip
# Link -> https://wd5.myworkdaysite.com/recruiting/microchiphr/External?locationCountry=f2e609fe92974a55a05fc1cdc2852122
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import re

session = requests.Session()


def get_ids() -> tuple:

    response = session.head(
        url='https://wd5.myworkdaysite.com/wday/cxs/microchiphr/External/jobs',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS01292a30=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response))
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, ts_id, wday_vps, wd_browser_id


def get_jobs():

    list_jobs = []
    data = get_ids()

    url = "https://wd5.myworkdaysite.com/wday/cxs/microchiphr/External/jobs"

    payload = {
        "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    headers = {
        "cookie": f"{data[0]}{data[1]}{data[2]}{data[3]}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    response = requests.request("POST", url, json=payload, headers=headers).json()['jobPostings']

    for job in response:
        city = ''
        location = job['locationsText']
        title = job['title']
        link = 'https://wd5.myworkdaysite.com/en-US/recruiting/microchiphr/External' + job['externalPath']

        if 'Bucharest' in location or 'Locations' in location:
            city = 'Bucharest'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Microchip",
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


company_name = 'Microchip'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Microchip',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Microchip-Logo.svg/744px-Microchip-Logo.svg.png'
                  ))