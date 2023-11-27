#
# Company - > konecranes
# Link ->https://careers.konecranes.com/Konecranes/search/?createNewAlert=false&q=&locationsearch=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_soup(url):

    r = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_jobs():

    list_jobs = []
    jobs = get_soup('https://careers.konecranes.com/Konecranes/search/?createNewAlert=false&q=&locationsearch=Romania'
                    ).find_all('tr', class_='data-row')

    for job in jobs:
        link = 'https://careers.konecranes.com' + job.find('a', class_='jobTitle-link')['href']
        city = job.find('span', class_='jobLocation').text.split(',')[0].strip()
        title = job.find('a', class_='jobTitle-link').text
        try:
            job_type = get_soup(link).find('span', attrs={'data-careersite-propertyid': 'customfield5'}).text.strip()
        except:
            job_type = 'on-site'
        print(job_type)
        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "konecranes",
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

company_name = 'konecranes'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('konecranes',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Konecranes-Logo.svg/250px-Konecranes-Logo.svg.png?20140815081543'
                  ))
