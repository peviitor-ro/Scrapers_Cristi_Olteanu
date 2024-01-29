#
# Company - > S and P
# Link -> https://careers.spglobal.com/jobs?locations=Bucharest,Bucure%C5%9Fti,Romania&page=1
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests


def get_json(page):
    url = "https://careers.spglobal.com/api/jobs"
    querystring = {"locations": "Bucharest,Bucureşti,Romania", "page": f"{page}", "sortBy": "relevance",
                   "descending": "false", "internal": "false"}
    payload = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    return requests.request("GET", url, data=payload, headers=headers, params=querystring).json()


def get_num_pages():

    num_jobs = get_json(1)['totalCount']
    pages = int(num_jobs/10)
    if num_jobs % 10 > 0:
        pages += 1
    else:
        pass
    return pages


def get_jobs():

    list_jobs = []
    for page in range(1, get_num_pages()+1, 1):

        response = get_json(page)['jobs']

        for job in response:
            city = job['data']['city']

            list_jobs.append({
                "job_title": job['data']['title'],
                "job_link": job['data']['meta_data']['canonical_url'],
                "company": "SandP",
                "country": "Romania",
                "city": city
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'SandP'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('S&P',
                  'https://companieslogo.com/img/orig/SPGI-23d836fa.png?t=1651808338'
                  ))

