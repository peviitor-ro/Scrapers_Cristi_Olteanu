#
# Company - > S and P
# Link -> https://careers.spglobal.com/jobs?locations=Bucharest,Bucure%C5%9Fti,Romania&page=1
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests


API_URL = "https://spgi.wd5.myworkdayjobs.com/wday/cxs/spgi/SPGI_Careers/jobs"


def get_jobs_from_workday(offset=0, limit=20):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "limit": limit,
        "offset": offset,
        "searchText": "",
    }
    resp = requests.post(API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_jobs():

    list_jobs = []
    offset = 0
    limit = 20

    while True:
        data = get_jobs_from_workday(offset, limit)
        for job in data.get("jobPostings", []):
            locations_text = job.get("locationsText", "")
            if "Bucharest" in locations_text or "Bucure" in locations_text or "Romania" in locations_text:
                list_jobs.append({
                    "job_title": job["title"],
                    "job_link": "https://spgi.wd5.myworkdayjobs.com" + job["externalPath"],
                    "company": "SandP",
                    "country": "Romania",
                    "city": "Bucuresti",
                    "county": "Bucuresti",
                    "remote": "on-site",
                })
        total = data.get("total", 0)
        offset += limit
        if offset >= total:
            break

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

