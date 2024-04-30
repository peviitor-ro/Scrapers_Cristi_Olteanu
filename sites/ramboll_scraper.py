#
#  Company - > Ramboll
# Link -> https://careers.smartrecruiters.com/Ramboll3
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []
    page = 0
    flag = True
    url = "https://careers.smartrecruiters.com/Ramboll3/api/more"

    while flag:

        querystring = {"search": "Romania", "type": "location", "value": "București, RO", "page": f"{page}"}
        response = requests.get(url=url, headers=DEFAULT_HEADERS, params=querystring)

        soup = BeautifulSoup(response.text, 'lxml')
        jobs = soup.find_all('li', class_='opening-job job column wide-7of16 medium-1of2')

        if len(jobs) > 0:

            for job in jobs:
                link = job.find('a', class_='link--block details')['href']
                title = job.find('h4', class_='details-title job-title link--block-target').text

                list_jobs.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "Ramboll",
                    "country": "Romania",
                    "city": 'Bucuresti',
                    "county": 'Bucuresti',
                    "remote": 'on-site'
                })
            page += 1
        else:
            flag = False
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'Ramboll'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Ramboll',
                  'https://c.smartrecruiters.com/sr-careersite-image-prod-aws-dc5/61976143f5f3344e7268f31e/42b2a37d-0498-4fdd-adaf-106bf49c17fe?r=s3-eu-central-1'
                  ))