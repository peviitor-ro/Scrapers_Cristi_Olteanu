#
#  Company - > Ramboll
# Link -> https://careers.smartrecruiters.com/Ramboll3
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
import json


def get_jobs():

    list_jobs = []
    url = "https://careers.smartrecruiters.com/Ramboll3"

    response = requests.get(url=url, headers=DEFAULT_HEADERS)

    try:
        data = response.json()
    except json.JSONDecodeError:
        return list_jobs

    if isinstance(data, dict):
        content = data.get('content', [])
        for job in content:
            link = job.get('url', '')
            title = job.get('title', '')
            location = job.get('location', {})

            if link and title:
                list_jobs.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "Ramboll",
                    "country": "Romania",
                    "city": location.get('city', 'Bucuresti') or 'Bucuresti',
                    "county": location.get('region', 'Bucuresti') or 'Bucuresti',
                    "remote": 'on-site'
                })

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
