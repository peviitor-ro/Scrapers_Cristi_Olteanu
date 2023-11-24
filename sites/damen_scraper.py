#
#  Company - > DAMEN
# Link -> https://career.damen.com/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()


def get_cookies():

    response = session.head(
        url='https://career.damen.com/wp-admin/admin-ajax.php',
    ).headers
    phpsessid = re.search(r"PHPSESSID=([^;]+);", str(response)).group(0)
    return phpsessid


def prepare_post():

    url = "https://career.damen.com/wp-admin/admin-ajax.php"

    payload = ("action=lumesse_ajax_grid_list&"
               "lanugage=1&params%5B0%5D%5Bkey%"
               "5D=customField1&params"
               "%5B0%5D%5Bval"
               "%5D=Romania&params%5B0%5D%5Bhidden%5D=false&params%5B1%5D%5Bkey%"
               "5D=date&params%5B1%5D%5Bval%5D=all&params%5B2%5D%5Bkey"
               "%5D=keywords&params%5B2%5D%5Bval%5D=&params%5B3%5D%5Bkey"
               "%5D=sort&params%5B3%5D%5Bval%5D=recent&params%5B4%5D%5Bkey%"
               "5D=page_job&params%5B4%5D%5Bval%5D=1&params%5B5%5D%5Bkey%"
               "5D=per_page&params%5B5%5D%5Bval%5D=9&sendEvent=false")
    headers = {
        "cookie": f"{get_cookies()}",
        "authority": "career.damen.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "csod-accept-language": "en-GB",
        "origin": "https://career.damen.com",
        "referer": "https://career.damen.com/",
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
    response = session.request("POST", data[0], data=data[1], headers=data[2]).json()['advertsHtml']
    soup = BeautifulSoup(response, 'lxml')
    jobs = soup.find_all('li', class_='col-lg-4 col-md-4 col-sm-6 col-xs-12')

    for job in jobs:
        title = job.find('a', class_='aa-item').text
        link = job.find('a', class_='aa-item')['href']
        city = job.find('span', class_='cs-location').text.split()[-1].strip()


        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "DAMEN",
            "country": "Romania",
            "city": city,
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'DAMEN'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('DAMEN',
                  'https://www.lumesse-engage.com/damen/wp-content/uploads/sites/76/2019/12/damen_blue_logo-1.png'
                  ))
