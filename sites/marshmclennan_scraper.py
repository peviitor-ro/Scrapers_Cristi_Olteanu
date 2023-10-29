#
# Company - > MarshMclennan
# Link -> https://careers.marshmclennan.com/global/en/search-results?keywords=&p=ChIJw3aJlSb_sUARlLEEqJJP74Q&location=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import re
import requests
import uuid

session = requests.Session()


def get_cookies() -> tuple:

    response = session.head(
        url='https://careers.marshmclennan.com/widgets',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group(0)
    return play_session, phpppe_act

def prepare_post():

    cookies = get_cookies()
    url = "https://careers.marshmclennan.com/widgets"

    payload = {
        "lang": "en_global",
        "deviceType": "desktop",
        "country": "global",
        "pageName": "search-results",
        "ddoKey": "eagerLoadRefineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": ["category", "country", "state", "city", "timeType", "business", "workFromHome", "campus", "jobType", "phLocSlider"],
        "size": 100,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": True,
        "pageId": "page23",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": {"country": ["Romania"]},
        "locationData": {
            "sliderRadius": 25,
            "aboveMaxRadius": False,
            "LocationUnit": "miles"
        },
        "s": "1"
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{cookies[0]}{cookies[1]}",
        "Origin": "https://careers.marshmclennan.com",
        "Referer": "https://careers.marshmclennan.com/global/en/search-results",
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

    response = requests.request("POST", data[0], json=data[1], headers=data[2]
                                ).json()['eagerLoadRefineSearch']['data']['jobs']

    for job in response:
        title = job['title']
        city = job['city']
        link = 'https://careers.marshmclennan.com/global/en/job/' + job['jobId']

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "MarshMclennan",
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


company_name = 'MarshMclennan'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('MarshMclennan',
                  'https://cdn.phenompeople.com/CareerConnectResources/prod/MAMCGLOBAL/images/1671010331095_MarshMcLennan_h_rgb_c-1615775108960.svg'
                  ))

