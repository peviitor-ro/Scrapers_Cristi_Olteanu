#
#  Company - > Conduent
# Link -> https://careers.conduent.com/us/en/search-results
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import re
import requests
from _county import get_county

session = requests.Session()


def get_cookies():

    response = session.head(
        url='https://careers.conduent.com/widgets',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group(0)

    return play_session, phpppe_act


def prepare_post():

    cookies = get_cookies()
    url = "https://careers.conduent.com/widgets"

    payload = {
        "lang": "en_us",
        "deviceType": "desktop",
        "country": "us",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": ["category", "country", "state", "city", "type", "remote"],
        "size": 100,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page20",
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
        "Origin": "https://careers.conduent.com",
        "Referer": "https://careers.conduent.com/us/en/search-results",
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
        link = 'https://careers.conduent.com/us/en/job/' + job['jobId']
        city = job['city']

        if 'Remote Romania' in city or city=='':
            city = 'Iasi'
            job_type = 'remote'
        elif 'remote' in title.lower().strip('('):
            job_type = 'remote'
        else:
            job_type = 'on-site'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Conduent",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": job_type
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'Conduent'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Conduent',
                  'https://cdn.phenompeople.com/CareerConnectResources/COJCONUS/images/Conduent_logo-1668514821347.svg'
                  ))

