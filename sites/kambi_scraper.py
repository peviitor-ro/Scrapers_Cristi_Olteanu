#
# Company - > Kambi
# Link ->https://boards.eu.greenhouse.io/kambi
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county
from _validate_city import validate_city


def get_soup(url):

    r = requests.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_jobs():

    jobs = get_soup('https://boards.eu.greenhouse.io/kambi').find_all('div',class_='opening')

    list_jobs = []

    for job in jobs:
        city = job.find('span').text

        if city == 'Bucharest':
            link = 'https://boards.eu.greenhouse.io/' + job.find('a')['href']
            title = job.find('a').text
            try:
                job_text = get_soup(link).find_all('strong')[2].text.split()[0]
            except:
                job_text = ''
            if 'Remote' in job_text:
                job_type = 'remote'
            elif 'Hybrid' in job_text:
                job_type = 'hibrid'
            else:
                job_type = 'on-site'
            city = validate_city(city)

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Kambi",
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


company_name = 'Kambi'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Kambi',
                  'https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/043/510/resized/Kambi_Logo_2023.png?1673968948'
                  ))

