#
#
#  Company - > ECOLAB
# Link -> https://jobs.ecolab.com/job-search-results/?location=Rom%C3%A2nia&country=RO&radius=25
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import re
import requests

session = requests.Session()


def get_cookies():

    response = session.head(
        url="https://ecolab.wd1.myworkdayjobs.com/wday/cxs/ecolab/Ecolab_External/jobs",
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    ts = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response))
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, ts, wday_vps, wd_browser_id


def prepare_post():

    cookies = get_cookies()
    url = "https://ecolab.wd1.myworkdayjobs.com/wday/cxs/ecolab/Ecolab_External/jobs"

    payload = {
        "appliedFacets": {"locations": ["88d5fb29f85801018b6c2ac810e20000", "292b680d80510154ed793effa574d767",
                                        "8ad79cd2b0580101f03004df87fb0000"]},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": f"{cookies[0]}{cookies[1]}{cookies[2]}{cookies[3]}",
        "Origin": "https://ecolab.wd1.myworkdayjobs.com",
        "Referer": "https://ecolab.wd1.myworkdayjobs.com/en-US/Ecolab_External?",
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

    response = session.request("POST", data[0], json=data[1], headers=data[2]).json()['jobPostings']

    for job in response:
        title = job['title']
        link = 'https://ecolab.wd1.myworkdayjobs.com/en-US/Ecolab_External' + job['externalPath']
        location = job['locationsText']
        city = location.split('-')[-1].strip()

        if 'locations' in location.lower():
            additional_locations = session.get(f"https://ecolab.wd1.myworkdayjobs.com/wday/cxs/ecolab/Ecolab_External{job['externalPath']}",
                                               headers=data[2]).json()['jobPostingInfo']['additionalLocations']
            for additional_location in additional_locations:
                if 'ROU' in additional_location:
                    city = additional_location.split('-')[-1].strip()


        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "ECOLAB",
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


company_name = 'ECOLAB'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('ECOLAB',
                  'https://cdn-static.findly.com/wp-content/uploads/sites/2650/2023/02/06034713/Ecolab_Logo_Blue_RGB-1.png'
                  ))



