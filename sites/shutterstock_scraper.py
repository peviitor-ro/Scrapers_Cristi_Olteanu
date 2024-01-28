#
# Company - > shutterstock
# Link -> https://careers.shutterstock.com/us/en/search-results
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import re

session = requests.Session()


def get_cookies():

    response = session.head(
        url= "https://careers.shutterstock.com/widgets",
        headers=DEFAULT_HEADERS
    ).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group(0)

    return play_session, phpppe_act


def prepare_post():

    cookies = get_cookies()
    url = "https://careers.shutterstock.com/widgets"

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
        "all_fields": ["category", "country", "state", "city", "type", "location", "remoteValue"],
        "size": 100,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page13",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": {"country": ["Romania"]},
        "locationData": {}
    }
    headers = {
        "authority": "careers.shutterstock.com",
        "accept": "*/*",
        "accept-language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "cookie": f"{cookies[0]}{cookies[1]}",
        "origin": "https://careers.shutterstock.com",
        "referer": "https://careers.shutterstock.com/us/en/search-results",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    return url, headers, payload


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = requests.request("POST", data[0], json=data[2], headers=data[1]).json()['refineSearch']['data']['jobs']

    for job in response:
        id = job['jobId']
        title = job['title']
        city = job['city'].split(',')[0]
        link = f'https://careers.shutterstock.com/us/en/job/{id}'

        for skill in job['ml_skills']:
            if 'hybrid' in skill:
                job_type = 'hybrid'
            else:
                job_type = 'on-site'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Shutterstock",
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


company_name = 'Shutterstock'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Shutterstock',
                  'https://logos-world.net/wp-content/uploads/2021/10/Shutterstock-Logo.png'
                  ))