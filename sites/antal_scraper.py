#
#  Company - > Antal
# Link -> https://www.antal.com/job-search/#/romania
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city

ANTAL_API = 'https://www.antal.com/_sf/api/v1/jobs/search.json'
DEFAULT_CITY = 'București'

CITY_CLEANUP = {
    'Pipera Metro Station, Bulevardul Dimitrie Pompeiu, București, România': 'București',
    'North - West, Romania': 'Cluj-Napoca',
    'Eastern Europe': DEFAULT_CITY,
}

ROMANIA_VARIANTS = {'romania', 'românia'}


def clean_city(raw_address):
    if not raw_address:
        return DEFAULT_CITY

    if raw_address in CITY_CLEANUP:
        return CITY_CLEANUP[raw_address]

    city = raw_address.split(',')[0].strip()

    if city.lower() in ROMANIA_VARIANTS:
        return DEFAULT_CITY

    return city


def get_jobs():
    list_jobs = []
    offset = 0
    jobs_per_page = 100

    while True:
        res = requests.post(
            ANTAL_API,
            json={
                "job_search": {
                    "query": "Romania",
                    "location": {},
                    "filters": {},
                    "commute_filter": {},
                    "offset": offset,
                    "jobs_per_page": jobs_per_page,
                    "salary_range": {}
                }
            },
            headers={'content-type': 'application/json'},
            timeout=30
        )

        if res.status_code != 200:
            break

        data = res.json()
        results = data.get('results', [])

        if not results:
            break

        for item in results:
            job = item.get('job', {})
            addresses = job.get('addresses', [])

            is_romania = False
            for cat in job.get('categories', []):
                if cat.get('name') == 'Country':
                    for v in cat.get('values', []):
                        if v.get('name', '').lower() in ROMANIA_VARIANTS:
                            is_romania = True

            if not is_romania:
                raw_addr = addresses[0] if addresses else ''
                if raw_addr.lower().strip() not in ROMANIA_VARIANTS:
                    continue

            raw_city = addresses[0] if addresses else ''
            city = clean_city(raw_city)
            city = validate_city(city)

            title = job.get('title', '')
            slug = job.get('url_slug', '')
            job_link = f'https://www.antal.com/job-search/{slug}'

            title_lower = title.lower()
            if 'remote' in title_lower:
                job_type = 'remote'
            elif 'hybrid' in title_lower or 'hibrid' in title_lower:
                job_type = 'hybrid'
            else:
                job_type = 'on-site'

            list_jobs.append({
                "job_title": title,
                "job_link": job_link,
                "company": "Antal",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": job_type
            })

        offset += jobs_per_page
        if offset >= data.get('total_size', 0):
            break

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Antal'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Antal',
                  'https://www.antal.com/app/public/images/logo.png'
                  ))
