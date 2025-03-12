#
#  Company - > gopro
# Link -> https://jobs.gopro.com/all-openings#/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from urllib.parse import unquote
from _validate_city import validate_city
from sites._county import get_county


def get_jobs():

    list_jobs = []
    session = requests.Session()
    base_url = "https://jobs.gopro.com"
    session.get(base_url)

    xsrf_token = unquote(session.cookies.get("XSRF-TOKEN", ""))
    laravel_session = session.cookies.get("laravel_session", "")

    url = "https://jobs.gopro.com/api/appSearch"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": base_url,
        "Referer": f"{base_url}/en/us/all-openings",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": xsrf_token,
        "Cookie": f"XSRF-TOKEN={xsrf_token}; laravel_session={laravel_session}"
    }

    payload = {"query": "",
               "search_fields": {"title": {}, "location": {}, "category": {}, "city_filter": {}, "country_filter": {}},
               "result_fields": {"title": {"raw": {}}, "location": {"raw": {}}, "job_type": {"raw": {}},
                                 "content": {"snippet": {"fallback": True}}, "category": {"raw": {}},
                                 "country_filter": {"raw": {}}, "city_filter": {"raw": {}}, "url": {"raw": {}}},
               "precision": 2, "page": {"size": 20, "current": 1}, "filters": {
            "all": [{"any": [{"location": "Bucharest"}]}, {"any": [{"group_id": 2082}]}, {"any": [{"live": 1}]}]},
               "facets": {"category": {"type": "value", "size": 30}, "location": {"type": "value", "size": 30},
                          "job_type": {"type": "value", "size": 30}}}

    jobs = session.post(url, headers=headers, json=payload).json()['results']

    for job in jobs:
        title = job['title']['raw']
        link = f"https://jobs.gopro.com/en/us/jobs/{job['url']['raw']}"
        city = validate_city(job['location']['raw'])
        job_type = job['job_type']['raw']
        county = get_county(city)

        list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "GoPro",
                "country": "Romania",
                "city": city,
                "county": county,
                "remote": job_type
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'GoPro'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('GoPro',
                  'https://1000logos.net/wp-content/uploads/2018/12/Gopro-Logo-500x313.png'
                  ))
