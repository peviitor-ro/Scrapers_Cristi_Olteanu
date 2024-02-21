#
#  Company - > expressvpn
# Link -> https://boards.greenhouse.io/embed/job_board?for=expressvpn&t=300df8672us&b=https%3A%2F%2Fwww.expressvpn.com%2Fjobs%2Fjob-openings
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():

    list_jobs = []

    response = requests.get('https://boards.greenhouse.io/embed/job_board?for=expressvpn&t=300df8672us&b=https%3A%2F%2Fwww.expressvpn.com%2Fjobs%2Fjob-openings',
                            headers=DEFAULT_HEADERS)

    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='opening')

    for job in jobs:
        link = job.find('a')['href']
        title = job.find('a').text
        city = job.find('span', class_='location').text

        if 'REMOTE' in city or 'Remote' in city:
            job_type = 'remote'
        else:
            job_type = 'on-site'

        if 'Bucharest' in city:
            city = 'Bucharest'

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "expressvpn",
                "country": "Romania",
                "city": city,
                "remote": job_type
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'expressvpn'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('expressvpn',
                  'https://upload.wikimedia.org/wikipedia/en/thumb/7/79/ExpressVPN-logo.svg/261px-ExpressVPN-logo.svg.png?20210118095637'
                  ))
