#
# Company - > qiagen
# Link -> https://www.qiagen.com/us/careers/jobs/index?searchCriteria[0][key]=LOV26&searchCriteria[0][values][]=16537&searchCriteria[1][key]=Resultsperpage&searchCriteria[1][values][]=50
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import re


def get_token():

    response = requests.get('https://www.qiagen.com/us/careers/jobs/index?searchCriteria[0][key'
                            ']=LOV26&searchCriteria[0][values][]=16537&searchCriteria[1][key'
                            ']=Resultsperpage&searchCriteria[1][values][]=50',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.find_all('script')

    for item in scripts:
        try:
            return item['data-lumesse-site-tech-id']
        except ValueError:
            pass


def get_cookies():

    response = requests.head(url='https://global3.recruitmentplatform.com/fo/rest/jobs?firstResult=0&maxResults='
                                 '50&sortBy=sJobTitle&sortOrder=asc', headers=DEFAULT_HEADERS)
    response_text = str(response.headers)

    cookie = re.search(r'AWSALBCORS=(.*?)(?:[;]|$)', response_text).group(0)
    return cookie


def prepare_post():

    token = get_token()
    cookies = get_cookies()

    url = "https://global3.recruitmentplatform.com/fo/rest/jobs"

    querystring = {"firstResult": "0", "maxResults": "50", "sortBy": "sJobTitle", "sortOrder": "asc"}

    payload = {"searchCriteria": {"criteria": [
        {
            "key": "LOV26",
            "values": ["16537"]
        },
        {
            "key": "Resultsperpage",
            "values": ["50"]
        }
    ]}}
    headers = {
        'authority': 'global3.recruitmentplatform.com',
        'method': 'POST',
        'path': '/fo/rest/jobs?firstResult=0&maxResults=50&sortBy=sJobTitle&sortOrder=asc',
        'scheme': 'https',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Length': '109',
        'Content-Type': 'application/json',
        'Cookie': f'{cookies}; EXPIRE_TIMESTAMP=1700581338303',
        'Lumesse-Language': 'EN',
        'Origin': 'https://www.qiagen.com',
        'Password': 'guest',
        'Referer': 'https://www.qiagen.com/',
        'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Username': f'{token}:guest:FO'
    }
    return url, payload, headers, querystring


def get_jobs():

    jobs_list = []
    data = prepare_post()

    response = requests.request("POST", data[0], json=data[1], headers=data[2], params=data[3]
                                ).json()['jobs']

    for job in response:
        title = job['jobFields']['jobTitle']
        city = job['jobFields']['SLOVLIST27']
        link = f"https://www.qiagen.com/us/about-us/careers/jobs/details?jobId={job['id']}&jobTitle="

        if 'Remote' in city:
            city = 'Cluj-Napoca'
            job_type = 'remote'
        else:
            job_type = 'on-site'

        jobs_list.append({
            "job_title": title,
            "job_link": link,
            "company": "qiagen",
            "country": "Romania",
            "city": city,
            "remote": job_type
        })
    return jobs_list

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'qiagen'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('qiagen',
                  'https://www.qiagen.com/sfc/images/qiagen-logo.png'
                  ))