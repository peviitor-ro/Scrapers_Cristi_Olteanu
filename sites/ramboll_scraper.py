#
#  Company - > Ramboll
# Link -> https://careers.smartrecruiters.com/Ramboll3
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county
from _validate_city import validate_city
import requests


SMARTRECRUITERS_API = 'https://api.smartrecruiters.com/v1/companies/Ramboll3/postings'


def get_jobs():
    list_jobs = []
    offset = 0
    page_size = 100

    while True:
        response = requests.get(
            SMARTRECRUITERS_API,
            params={'q': 'Romania', 'limit': page_size, 'offset': offset},
            headers=DEFAULT_HEADERS,
            timeout=30
        )

        if response.status_code != 200:
            break

        data = response.json()
        content = data.get('content', [])

        if not content:
            break

        for job in content:
            location = job.get('location', {})
            country = (location.get('country') or '').lower()
            if country != 'ro':
                continue

            job_id = job.get('id', '')
            title = job.get('name', '')
            link = f'https://careers.smartrecruiters.com/Ramboll3/jobs/{job_id}'
            raw_city = location.get('city', '')
            city = validate_city(raw_city)

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Ramboll",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": 'on-site'
            })

        offset += page_size
        if len(content) < page_size:
            break

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
