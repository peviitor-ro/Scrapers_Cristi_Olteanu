#
# Company - > danieli
# Link -> # https://www.danieli.com/en/europe-and-usa-opportunities.htm?searchCriteria[0][key]=COUN&searchCriteria[0][values][]=1249
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import re
from _county import get_county


def get_token():

    response = requests.get('https://www.danieli.com/en/europe-and-usa-opportunities.htm?searchCriteria[0][key]=COUN&searchCriteria[0][values][]=1249',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.find_all('script')

    for item in scripts:
        try:
            return item['data-talentlink-fo-site-tech-id']
        except:
            pass


def get_cookies():

    response = requests.head(
        url='https://emea3.recruitmentplatform.com/fo/rest/jobs?firstResult=0&maxResults=12&sortBy=DPOSTINGSTART&sortOrder=asc',
    headers=DEFAULT_HEADERS)
    response_text = str(response.headers)

    cookie = re.search(r'AWSALBCORS=(.*?)(?:[;]|$)', response_text).group(0)
    return cookie


def prepare_post():

    token = get_token()
    cookies = get_cookies()

    url = "https://emea3.recruitmentplatform.com/fo/rest/jobs"

    querystring = {"firstResult": "0", "maxResults": "12", "sortBy": "DPOSTINGSTART", "sortOrder": "asc"}

    payload = {"searchCriteria": {"criteria": [
        {
            "key": "COUN",
            "values": ["1249"]
        }
    ]}}
    headers = {

        "authority": "emea3.recruitmentplatform.com",
        "method": "POST",
        "path": "/fo/rest/jobs?firstResult=0&maxResults=12&sortBy=DPOSTINGSTART&sortOrder=asc",
        "scheme": "https",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Length": "66",
        "Content-Type": "application/json",
        "Cookie": f"{cookies}; EXPIRE_TIMESTAMP=1699901146743",
        "Lumesse-Language": "UK",
        "Origin": "https://www.danieli.com",
        "Password": "guest",
        "Referer": "https://www.danieli.com/",
        "Sec-Ch-Ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Username": f"{token}:guest:FO"
    }
    return url, payload, headers, querystring


def get_jobs():

    list_jobs = []
    data = prepare_post()

    response = requests.request("POST", data[0], json=data[1], headers=data[2], params=data[3]
                                ).json()
    if response['globals']['jobsCount'] > 0:
        for job in response['jobs']:
            title = job['jobFields']['jobTitle']
            city = job['jobFields']['SLOVLIST2']
            link = f"https://www.danieli.com/en/europe-and-usa-opportunities.htm?languageSelect=UK&jobId={job['id']}&jobTitle="

            if 'Cluj Napoca' in city:
                city = 'Cluj-Napoca'

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "danieli",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": 'on-site'
            })
    else:
        pass

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'danieli'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('danieli',
                  'https://www.danieli.com/media/assets/logo_danieli.svg'
                  ))



