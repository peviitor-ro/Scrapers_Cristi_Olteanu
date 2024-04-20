#
# Company - > GE
# Link -> https://jobs.gecareers.com/global/en/search-results?qcountry=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import re
import requests

session = requests.Session()


def get_cookies() -> tuple:

    response = session.head(
        url='https://jobs.gecareers.com/',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group()
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group()
    return play_session, phpppe_act


def prepare_post():

    cookies = get_cookies()
    url = "https://jobs.gecareers.com/widgets"
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
        "all_fields": ["business", "category", "jobFamilies", "country", "state", "city", "checkRemote",
                       "experienceLevel"],
        "size": 100,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page1",
        "siteType": "external",
        "keywords": "Romania",
        "global": True,
        "selected_fields": {},
        "locationData": {}
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{cookies[0]}{cookies[1]}",
        "Origin": "https://jobs.gecareers.com",
        "Referer": "https://jobs.gecareers.com/global/en/search-results?keywords=Romania",
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
                                ).json()['refineSearch']['data']['jobs']

    for job in response:
        title = job['title']
        city = job['city']
        link = 'https://jobs.gecareers.com/global/en/job/' + job['jobId']

        if city == 'Remote':
            city = 'Bucharest'
            job_type = 'remote'
        else:
            city = 'Bucharest'
            job_type = 'on-site'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "GE",
            "country": "Romania",
            "city": city,
            "remote": job_type
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'GE'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('GE',
                  'https://www.freepnglogos.com/uploads/ge-png-logo/general-electric-logo-png-4.png'
                  ))

