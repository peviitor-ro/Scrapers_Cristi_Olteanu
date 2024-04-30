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

    response = requests.get('https://careers.n-able.com/api/jobs?page=1&locations=Bucharest%252C%252CRomania&sortBy=relevance&descending=false&internal=false',
                            headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                            }
                            ).json()['jobs']

    for job in response:
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

