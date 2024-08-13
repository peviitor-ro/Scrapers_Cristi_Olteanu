#
# Company - > retarus
# Link -> # https://retarus-learning.csod.com/ux/ats/careersite/4/home/requisition/166?c=retarus-learning&lang=en-GB&source=LinkedIn
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county
import re


def get_token():

    response = requests.get('https://retarus-learning.csod.com/ux/ats/careersite/4/home?c=retarus-learning&country=ro&lang=en-GB&source=LinkedIn',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    pattern = r'"token":"(.*?)"'
    matches = re.findall(pattern, str(soup))
    token = matches[0]

    return token


def prepare_post():

    url = "https://eu-fra.api.csod.com/rec-job-search/external/jobs"

    payload = {
        "careerSiteId": 4,
        "careerSitePageId": 4,
        "pageNumber": 1,
        "pageSize": 25,
        "cultureId": 2,
        "searchText": "",
        "cultureName": "en-GB",
        "states": [],
        "countryCodes": ["ro"],
        "cities": [],
        "placeID": "",
        "radius": None,
        "postingsWithinDays": None,
        "customFieldCheckboxKeys": [],
        "customFieldDropdowns": [],
        "customFieldRadios": []
    }
    headers = {
        "authority": "eu-fra.api.csod.com",
        "accept": "application/json; q=1.0, text/*; q=0.8, */*; q=0.1",
        "accept-language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {get_token()}",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "csod-accept-language": "en-GB",
        "origin": "https://retarus-learning.csod.com",
        "referer": "https://retarus-learning.csod.com/",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    return url, payload, headers


def get_jobs():

    list_jobs = []
    data = prepare_post()
    try:
        response = requests.request("POST", data[0], json=data[1], headers=data[2]).json()['data']['requisitions']
    except:
        return []

    for job in response:

        title = job['displayJobTitle']
        link = f"https://retarus-learning.csod.com/ux/ats/careersite/4/home/requisition/{job['requisitionId']}?c=retarus-learning&lang=en-GB&source=LinkedIn"
        city = job['locations'][0]['city']

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "retarus",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": 'on-site'
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'retarus'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('retarus',
                  'https://retarus-learning-pilot.csod.com/clientimg/retarus-learning/logo/retaruslogo_dff060b8-d997-4db5-8f44-6ac045e64470.png'
                  ))
