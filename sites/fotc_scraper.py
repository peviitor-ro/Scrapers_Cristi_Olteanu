#
#  Company - > fotc
# Link -> https://fotc.jobsoid.com/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []
    response = requests.get('https://fotc.jobsoid.com/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='row')

    for job in jobs:
        text = job.find('a', class_='jobDetailsLink')
        try:
            link = 'https://fotc.jobsoid.com'+text.get('href')
        except:
            link = None

        if link is not None:
            title = text.text
            link = link
            location = job.find('span', class_='r-space').text.split('/')[0].strip()
            city = job.find('span', class_='r-space').text.split('/')[-1].strip()
            job_type = ''

            if 'Romania' in location:
                if 'remote' in city.lower():
                    job_type = 'remote'
                    city = 'Bucuresti'

                list_jobs.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "fotc",
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


company_name = 'fotc'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('fotc',
                  'https://fotc.jobsoid.com/PortalJob/GetPortalLogo?size=medium'
                  ))