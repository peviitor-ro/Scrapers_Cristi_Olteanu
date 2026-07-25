#
# Company - > Edurom
# Link -> https://www.edurom.ro/it-jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county

AJAX_URL = "https://www.edurom.ro/wp-admin/admin-ajax.php"
DEFAULT_CITY = 'Bucuresti'

CITY_MAP = {
    'Bucharest': 'Bucuresti',
    'Cluj': 'Cluj-Napoca',
    'Iasi': 'Iasi',
    'Timisoara': 'Timisoara',
}


def parse_location(loc_div):
    if not loc_div:
        return DEFAULT_CITY, 'on-site'

    terms = [t.text.strip() for t in loc_div.find_all('span', class_='awsm-job-specification-term')]

    job_type = 'on-site'
    cities = []

    for term in terms:
        lower = term.lower()
        if 'remote' in lower:
            job_type = 'remote'
        elif 'hybrid' in lower:
            job_type = 'hybrid'
        else:
            mapped = CITY_MAP.get(term, term)
            cities.append(mapped)

    city = cities[0] if cities else DEFAULT_CITY
    return city, job_type


def get_jobs():
    list_jobs = []

    payload = {
        "jq": "",
        "awsm_job_spec[job-type]": "",
        "awsm_job_spec[job-location]": "",
        "awsm_job_spec[job-level]": "",
        "awsm_job_spec[job-status]": "29",
        "action": "jobfilter",
        "listings_per_page": "200",
        "shortcode_specs": "job-category:18",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    response = requests.post(AJAX_URL, data=payload, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_='awsm-job-listing-item')

    for job in jobs:
        if 'awsm-job-filled-item' in job.get('class', []):
            continue

        title_el = job.find('h2', class_='awsm-job-post-title')
        link_el = job.find('a', class_='awsm-job-item')
        loc_div = job.find('div', class_='awsm-job-specification-item awsm-job-specification-job-location')

        if not title_el or not link_el:
            continue

        title = title_el.text.strip()
        job_link = link_el['href']
        city, job_type = parse_location(loc_div)

        list_jobs.append({
            "job_title": title,
            "job_link": job_link,
            "company": "Edurom",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": job_type
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Edurom'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Edurom',
                  'https://images.crunchbase.com/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/v1460910381/o5sxwffz8lb8h6dpbs2b.png'
                  ))
