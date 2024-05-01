#
#  Company - > mastercard
# Link -> https://careers.mastercard.com/us/en/search-results?qcountry=Romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import re
import requests

session = requests.Session()


def get_cookies() -> tuple:

    response = session.head(
        url='https://careers.mastercard.com/widgets',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group(0)
    return play_session, phpppe_act


def prepare_post():

    cookies = get_cookies()

    url = "https://careers.mastercard.com/widgets"

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
        "all_fields": ["category", "country", "state", "city", "postalCode", "jobType"],
        "size": 10,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page11",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": {"country": ["Romania"]}
    }
    headers = {
       "Accept": "application/json",
       "Accept-Language": "en-US",
       "Connection": "keep-alive",
       "Content-Type": "application/json",
       "Cookie": f"{cookies[0]}{cookies[1]}",
       "Origin": "https://careers.mastercard.com",
       "Referer": "https://careers.mastercard.com/us/en/search-results",
       "Sec-Fetch-Dest": "empty",
       "Sec-Fetch-Mode": "cors",
       "Sec-Fetch-Site": "same-origin",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
       "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
       "sec-ch-ua-mobile": "?0",
       "sec-ch-ua-platform": "Windows",
    }
    return url,payload,headers


def get_jobs():

    data = prepare_post()
    list_jobs = []
    response = requests.request("POST", data[0], json=data[1], headers=data[2]).json()['refineSearch']['data']['jobs']

    for job in response:
        title = job['title']
        link = 'https://careers.mastercard.com/us/en/job/' + job['jobId']

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "mastercard",
            "country": "Romania",
            "city": 'Bucuresti',
            "county": 'Bucuresti',
            "remote": 'on-site'
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'mastercard'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mastercard',
                  'https://cdn.vox-cdn.com/thumbor/tFVfkB8D8iB_dOZ-lVnZHaX4_X0=/0x0:1000x1000/920x613/filters:focal(421x430:581x590)/cdn.vox-cdn.com/uploads/chorus_image/image/62800797/Mastercard_logo.0.jpg'
                  ))

