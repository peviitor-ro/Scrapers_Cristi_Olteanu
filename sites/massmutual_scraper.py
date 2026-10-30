#
#  Company - > MassMutual
# Link -> https://massmutual.wd1.myworkdayjobs.com/en-US/MMROCareerSite
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city

BASE_URL = 'https://massmutual.wd1.myworkdayjobs.com'
CAREER_SITE = 'MMROCareerSite'
JOBS_URL = f'{BASE_URL}/wday/cxs/massmutual/{CAREER_SITE}/jobs'


def get_job_details(external_path):

    response = requests.get(
        f'{BASE_URL}/wday/cxs/massmutual/{CAREER_SITE}{external_path}',
        headers=DEFAULT_HEADERS)

    if response.status_code != 200:
        return None

    return response.json().get('jobPostingInfo', {})


def get_jobs():

    list_jobs = []
    offset = 0

    while True:
        response = requests.post(
            JOBS_URL,
            headers=DEFAULT_HEADERS,
            json={
                "appliedFacets": {},
                "limit": 20,
                "offset": offset,
                "searchText": ""
            }).json()

        job_postings = response.get('jobPostings', [])
        total = response.get('total', 0)

        for job in job_postings:
            details = get_job_details(job['externalPath']) or {}
            locations = [details.get('location', '')] + details.get('additionalLocations', [])

            cities = []
            for location in locations:
                if 'Romania' not in location:
                    continue
                city = validate_city(location.split(',')[0].strip())
                if city and city not in cities:
                    cities.append(city)

            if not cities:
                continue

            remote_type = details.get('remoteType', '')
            if 'hybrid' in remote_type.lower():
                remote = 'hybrid'
            elif 'remote' in remote_type.lower():
                remote = 'remote'
            else:
                remote = 'on-site'

            list_jobs.append({
                "job_title": job['title'],
                "job_link": f'{BASE_URL}/en-US/{CAREER_SITE}{job["externalPath"]}',
                "company": "MassMutual",
                "country": "Romania",
                "city": cities,
                "county": get_county(cities),
                "remote": remote
            })

        offset += len(job_postings)
        if not job_postings or offset >= total:
            break

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'MassMutual'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('MassMutual',
'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/MassMutual_logo.svg/512px-MassMutual_logo.svg.png'
                  ))

