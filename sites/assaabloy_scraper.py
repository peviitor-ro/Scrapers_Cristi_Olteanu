#
# Company - > assaabloy
# Link -> https://assaabloy.jobs2web.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_country=&optionsFacetsDD_state=&optionsFacetsDD_department=&optionsFacetsDD_lang=
#

from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    res = requests.get(
        'https://assaabloy.jobs2web.com/search/?searchby=location&createNewAlert=false&q=&locationsearch=Romania&geolocation=&optionsFacetsDD_country=&optionsFacetsDD_state=&optionsFacetsDD_department=&optionsFacetsDD_lang=',
        headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(res.text, 'lxml')

    list_jobs = []

    jobs = soup.find_all('tr', class_='data-row')

    for job in jobs:
        title = job.find('a', class_='jobTitle-link').text
        link = 'https://assaabloy.jobs2web.com/' + job.find('a', class_='jobTitle-link')['href']

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "assaabloy",
            "country": "Romania",
            "city": 'Bucuresti',
            "county": 'Bucuresti',
            "remote": 'on-site'
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'assaabloy'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('assaabloy',
                  'https://www.hpd-collaborative.org/wp-content/uploads/2019/07/ASSA-ABLOY-logo-300x200.jpg'
                  ))


