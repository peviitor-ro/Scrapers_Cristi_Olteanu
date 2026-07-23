#
# Company - > n-able
# Link -> https://careers.n-able.com/jobs
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
from _county import get_county
from  _validate_city import validate_city


def get_jobs():

    list_jobs = []

    try:
        response = requests.get('https://careers.n-able.com/api/jobs',
                                params={
                                    'page': 1,
                                    'locations': 'Bucharest,Romania',
                                    'sortBy': 'relevance',
                                    'descending': 'false',
                                    'internal': 'false',
                                })
        if response.status_code != 200:
            return list_jobs
        jobs_data = response.json()['jobs']
    except Exception:
        return list_jobs

    for job in jobs_data:
        city = validate_city(job['data']['city'])

        list_jobs.append({
            "job_title": job['data']['title'],
            "job_link": job['data']['meta_data']['canonical_url'],
            "company": "n-able",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": "hybrid"
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'n-able'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('n-able',
                  'https://companieslogo.com/img/orig/NABL_BIG-ab085fb0.png?t=1631222615'
                  ))

