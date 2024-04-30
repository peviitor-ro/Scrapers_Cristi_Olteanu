#
#  Company - > proctorandgamble
# Link -> https://www.pgcareers.com/global/en/search-results
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
import re
from _county import get_county
from _validate_city import validate_city

session = requests.Session()


def get_cookies():

    response = session.head(
        url="https://www.pgcareers.com/widgets",
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    phpppe_act = re.search(r"PHPPPE_ACT=([^;]+);", str(response)).group(0)

    return play_session, phpppe_act


def prepare_post():

    cookies = get_cookies()

    url = "https://www.pgcareers.com/widgets"

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
        "all_fields": ["category", "country", "state", "city", "type", "subCategory", "experienceLevel"],
        "size": 100,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page16",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": {"country": ["Romania"]},
        "locationData": {}
    }

    headers = {
        "authority": "www.pgcareers.com",
        "accept": "*/*",
        "accept-language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "cookie": f"{cookies[0]}{cookies[1]}",
        "origin": "https://www.pgcareers.com",
        "referer": "https://www.pgcareers.com/global/en/search-results?ascf=^[^{^%^27key^%^27:^%^27custom_fields.Language^%^27,^%^27value^%^27:^%^27English^%^27^},^]&alp=798549&alt=2",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    return url, payload, headers


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = requests.request("POST", data[0], json=data[1], headers=data[2]).json()['refineSearch']['data']['jobs']

    for job in response:
        title = job['title']
        city = job['city']
        link = 'https://www.pgcareers.com/global/en/job/' + job['jobId']

        if city != 'Urlati' and city != 'Bucharest':
            try:
                multi_location = job['multi_location']
                for location in multi_location:
                    if 'Romania' in location:
                        city = location.split(',')[0]
            except:
                pass
        city = validate_city(city)

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "proctorandgamble",
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

company_name = 'proctorandgamble'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('proctorandgamble',
                  'https://logos-world.net/wp-content/uploads/2022/11/PG-Symbol.png'
                  ))


