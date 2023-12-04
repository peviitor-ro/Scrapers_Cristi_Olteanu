#
# Company - > KuehneNagel
# Link -> https://jobs.kuehne-nagel.com/global/en/search-results?qcountry=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import re
import requests
import uuid

session = requests.Session()


def get_cookies():

    response = session.head(
        url='https://jobs.kuehne-nagel.com/global/en/search-results?keywords=Romania',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    ts = re.search(r"TS0181aecd=([^;]+);", str(response)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group(0)

    return play_session, phpppe_act, ts


def prepare_post():

    cookies = get_cookies()
    url = "https://jobs.kuehne-nagel.com/widgets"

    payload = {
        "lang": "en_global",
        "deviceType": "desktop",
        "country": "global",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": ["country", "state", "city", "category", "CareerLevel", "type", "WorkType", "remote"],
        "size": 15,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page3",
        "siteType": "external",
        "keywords": "Romania",
        "global": True,
        "selected_fields": {"country": ["Romania"]},
        "locationData": {}
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{cookies[0]}{cookies[1]}{cookies[2]}",
        "Origin": "https://jobs.kuehne-nagel.com",
        "Referer": "https://jobs.kuehne-nagel.com/global/en/search-results?keywords=Romania",
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

    response = session.request("POST", data[0], json=data[1], headers=data[2]
                               ).json()['refineSearch']['data']['jobs']

    for job in response:
        title = job['title']
        link = 'https://jobs.kuehne-nagel.com/global/en/job/' + job['reqId']
        city = job['city']

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "KuehneNagel",
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


company_name = 'KuehneNagel'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('KuehneNagel',
                  'https://cdn.phenompeople.com/CareerConnectResources/KUNAGLOBAL/nl_nl/desktop/assets/images/knglobal-careers-logo.png'
                  ))
