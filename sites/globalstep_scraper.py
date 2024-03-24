#  Company - > globalstep
# Link -> https://globalstep.com/careers-detail-page/?job__location_spec=romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup

session = requests.Session()


def prepare_post(page: str):

    url = "https://globalstep.com/wp-admin/admin-ajax.php"

    payload = f"action=loadmore&paged={page}&listings_per_page=20&lang=en"

    headers = {
        'authority': 'globalstep.com',
        'accept': '/',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://globalstep.com',
        'referer': 'https://globalstep.com/careers-detail-page/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    return url, payload, headers


def get_jobs():

    list_jobs = []

    page = 0
    flag = True

    while flag:

        data = prepare_post(str(page))

        response = session.request("POST", data[0], data=data[1], headers=data[2])

        soup = BeautifulSoup(response.text, 'lxml')
        jobs = soup.find_all('div', class_='awsm-job-listing-item awsm-grid-item')

        if len(jobs) > 0:

            for job in jobs:
                link = job.find('a', class_='awsm-job-item')['href']
                title = job.find('h2', class_='awsm-job-post-title').text.strip()
                text = job.find('span', class_='awsm-job-specification-term').text
                city = text.split('-')[0].strip()

                if 'Romania' in text:
                    list_jobs.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "globalstep",
                        "country": "Romania",
                        "city": city,
                    })

        else:
            flag = False
        page += 1

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'globalstep'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('globalstep',
                  'https://mma.prnewswire.com/media/1394631/GlobalStep_Logo.jpg?w=200'
                  ))
