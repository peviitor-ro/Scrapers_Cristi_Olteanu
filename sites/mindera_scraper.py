#
#  Company - > mindera
# Link -> https://apply.workable.com/minderacraft/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
import re
from _county import get_county

session = requests.Session()


def get_cookies() -> tuple:

    response = session.head(
        url='https://apply.workable.com/minderacraft/',
        headers=DEFAULT_HEADERS).headers
    wmc = re.search(r"wmc=([^;]+);", str(response)).group(0)
    cf_bm = re.search(r"__cf_bm=([^;]+);", str(response)).group(0)

    return wmc, cf_bm


def prepare_post():

    cookies = get_cookies()
    url = "https://apply.workable.com/api/v3/accounts/minderacraft/jobs"

    payload = {
        "query": "",
        "location": [
            {
                "country": "Romania",
                "region": "Cluj County",
                "city": "Cluj-Napoca",
                "countryCode": "RO"
            }
        ],
        "department": [],
        "worktype": [],
        "remote": [],
        "workplace": []
    }
    headers = {
        'authority': 'apply.workable.com',
        'scheme': 'https',
        'Accept': 'application/json',
        'Accept-Language': 'en',
        'Content-Length': '167',
        'Content-Type': 'application/json',
        'Cookie': f'{cookies[0]}{cookies[1]}',
        'Origin': 'https://apply.workable.com',
        'Referer': 'https://apply.workable.com/minderacraft/',
        'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    return url, payload, headers


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = session.request("POST", data[0], json=data[1], headers=data[2]).json()['results']

    for job in response:
        title = job['title']
        city = job['location']['city']
        job_type = job['workplace']
        link = f"https://apply.workable.com/minderacraft/j/{job['shortcode']}/"

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "mindera",
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

company_name = 'mindera'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mindera',
                  'https://www.cbpecapital.com/wp-content/uploads/mindera-logo-1@3x-480x295.png'
                  ))












