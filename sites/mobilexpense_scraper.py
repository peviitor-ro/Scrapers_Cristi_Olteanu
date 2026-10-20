#
# Company - > mobilexpense
# Link -> https://mobilexpense.recruitee.com/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():
    list_jobs = []

    response = requests.get('https://mobilexpense.recruitee.com/api/offers/', headers=DEFAULT_HEADERS)
    jobs = response.json()['offers']

    for job in jobs:
        city = validate_city(job.get('city'))
        if job.get('remote'):
            remote = 'remote'
        elif job.get('hybrid'):
            remote = 'hybrid'
        else:
            remote = 'on-site'

        list_jobs.append({
            "job_title": job.get('title'),
            "job_link": job.get('careers_url'),
            "company": "mobilexpense",
            "country": job.get('country'),
            "city": city,
            "county": get_county(city),
            "remote": remote
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'mobilexpense'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mobilexpense',
                  'https://careers.recruiteecdn.com/image/upload/q_auto,f_auto,w_400,c_limit/production/images/A2Dv/1EA9BGIlGXOu.png'
                  ))