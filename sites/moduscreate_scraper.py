#
# Company - > ModusCreate
# Link -> https://moduscreate.com/careers/?gh_src=504950c63us
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests


def get_jobs():

    url = "https://boards-api.greenhouse.io/v1/boards/moduscreate/jobs/?content=true"

    querystring = {"content": "true"}

    headers = {
        "Content-Type": "application/json",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()['jobs']

    list_jobs = []

    for job in response:

        link = job['absolute_url']
        title = job['title']

        if 'Romania' in job['location']['name']:
            city = 'Cluj-Napoca'

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "ModusCreate",
                "country": "Romania",
                "city": city,
                "county": 'Cluj',
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'ModusCreate'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('ModusCreate',
                  'https://www.pngfind.com/pngs/m/313-3132250_welcome-to-our-job-board-take-a-spin.png'
                  ))