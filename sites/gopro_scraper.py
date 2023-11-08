#
#  Company - > gopro
# Link -> https://jobs.gopro.com/all-openings#/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

sessions = requests.Session()


def get_soup(url):

    response = sessions.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_jobs():

    list_jobs = []
    url = "https://jobs.gopro.com/api/v1/jobs/external"

    payload = {
        "group": "gopro",
        "group_id": "1613",
        "filters": "{}",
        "query": "Romania'",
        "from": 0,
        "mobile": 0,
        "session": "",
        "old_search": 0}

    response = sessions.post(url, json=payload, headers=DEFAULT_HEADERS
                             ).json()['response']['matchingJobs']

    for job in response:
        title = job['jobTitleSnippet']
        link = str(job['job']['customAttributes']['url']['stringValues'][0]).replace('http','https')

        location_headline = get_soup(link).find('div', class_='col-md-7').find('h5').text

        if 'flexible' in location_headline.lower():
            job_type = 'hybrid'
        elif 'remote' in location_headline.lower():
            job_type = 'remote'
        else:
            job_type = 'on-site'

        list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "GoPro",
                "country": "Romania",
                "city": 'Bucuresti',
                "remote": job_type
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'GoPro'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('GoPro',
                  'https://1000logos.net/wp-content/uploads/2018/12/Gopro-Logo-500x313.png'
                  ))
