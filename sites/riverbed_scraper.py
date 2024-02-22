#
# Company - > Riverbed
# Link -> https://careers.riverbed.com/jobs?stretchUnits=MILES&stretch=10&location=Romania&lat=46&lng=25&woe=12
from A_OO_get_post_soup_update_dec import update_peviitor_api , DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []
    url = "https://emea-apj-riverbed.icims.com/jobs/search"
    querystring = {"ss": "1", "searchLocation": "13526", "in_iframe": "1"}

    response = requests.request("GET", url, headers=DEFAULT_HEADERS, params=querystring)

    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='row')

    for job in jobs:
        link_text = job.find('a')
        if link_text is not None:
            link = link_text['href']
            title = job.find('h3').text.strip()
            location_text = job.find('div', class_='col-xs-6 header left').text

            if 'RO-Home Office' in location_text:
                job_type = 'remote'
            else:
                job_type = 'hibrid'

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Riverbed",
                "country": "Romania",
                "city": 'Cluj-Napoca',
                "remote": job_type
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Riverbed'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Riverbed',
                  'https://cms.jibecdn.com/prod/riverbed/assets/HEADER-LOGO_IMG-en-us-1649182997894.png'
                  ))

