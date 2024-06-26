#
# Company - > VictorySquare
# Link -> https://victorysquarepartners.com/careers/job-opportunities/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county


def get_jobs():

    list_jobs = []
    response = requests.get('https://victorysquarepartners1.recruitee.com/api/offers/',
                            headers=DEFAULT_HEADERS).json()['offers']

    for job in response:

        title = job['title']
        city = job['city']
        location = job['location']
        link = job['careers_url']

        if 'Remote' in location:
            job_type = 'remote'
        else:
            job_type = 'on-site'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "VictorySquare",
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


company_name = 'VictorySquare'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('VictorySquare',
                  'https://victorysquarepartners.com/wp-content/uploads/2022/06/VSP-Logo-SVG.svg'
                  ))