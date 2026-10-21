#
# Company - > Picsart
# Link -> https://picsart.com/careers/jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county
from _validate_city import validate_city


# API-ul folosit de insusi site-ul de cariere picsart.com pentru lista de joburi
JOBS_API = 'https://api.picsart.com/careers/jobs/raw'
# Detaliile unui singur job (folosite doar daca lista nu contine descrierea)
JOB_DETAILS_API = 'https://api.picsart.com/careers/jobs/raw/'
# Tabla Greenhouse pe care site-ul o embedeaza (rezerva)
GREENHOUSE_API = 'https://boards-api.greenhouse.io/v1/boards/picsart/jobs'
# Pagina oficiala a unui job
JOB_LINK = 'https://picsart.com/careers/job/'

# Picsart publica joburi in mai multe tari, dar pe peviitor.ro se trimit
# doar cele din Romania (Bucuresti)
ROMANIA_MARKERS = ('romania', 'bucharest', 'bucuresti')


def get_jobs_from_api():
    """
    Lista oficiala de joburi, exact cum o cere site-ul picsart.com.
    """

    try:
        response = requests.get(JOBS_API, headers=DEFAULT_HEADERS, timeout=30)
    except Exception:
        return []

    if response.status_code != 200:
        return []

    try:
        jobs = response.json()
    except Exception:
        return []

    return jobs if isinstance(jobs, list) else []


def get_jobs_from_greenhouse():
    """
    Rezerva: tabla Greenhouse din spatele job board-ului de pe picsart.com.
    """

    try:
        response = requests.get(GREENHOUSE_API, headers=DEFAULT_HEADERS, timeout=30)
    except Exception:
        return []

    if response.status_code != 200:
        return []

    try:
        payload = response.json()
    except Exception:
        return []

    jobs = []
    for job in payload.get('jobs', []):
        location = (job.get('location') or {}).get('name') or ''
        jobs.append({
            'id': job.get('id'),
            'title': job.get('title'),
            'city': location.split(',')[0].strip(),
            'location': location,
            'description': ''
        })
    return jobs


def get_all_jobs():

    jobs = get_jobs_from_api()

    if jobs:
        return jobs

    return get_jobs_from_greenhouse()


def get_description(job):

    description = job.get('description')

    if not description:
        job_id = str(job.get('id') or '')
        try:
            response = requests.get(JOB_DETAILS_API + job_id, headers=DEFAULT_HEADERS, timeout=30)
            if response.status_code == 200:
                description = response.json().get('description')
        except Exception:
            description = None

    return description or ''


def get_job_types(description):

    soup = BeautifulSoup(description, 'lxml').getText().lower()

    if 'hybrid' in soup:
        job_type_ = 'hybrid'
    elif 'remote' in soup:
        job_type_ = 'remote'
    else:
        job_type_ = 'on-site'
    return job_type_


def is_romanian(job):
    """
    Locatia poate fi 'Bucharest, Romania', 'Romania' sau doar 'Bucharest',
    de aceea se verifica tot textul locatiei, nu doar ultima bucata.
    """

    location = ' '.join([str(job.get('location') or ''), str(job.get('city') or '')]).lower()

    return any(marker in location for marker in ROMANIA_MARKERS)


def get_city(job):

    city = (job.get('city') or '').strip()

    if not city:
        city = (job.get('location') or '').split(',')[0].strip()

    return validate_city(city)


def get_jobs():

    list_jobs = []

    for job in get_all_jobs():

        if not is_romanian(job):
            continue

        city = get_city(job)

        if not city:
            continue

        job_id = str(job.get('id') or '')

        list_jobs.append({
            "job_title": job.get('title'),
            "job_link": JOB_LINK + job_id + '/',
            "company": "Picsart",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": get_job_types(get_description(job))
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Picsart'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Picsart',
                  'https://1000logos.net/wp-content/uploads/2022/11/Picsart-Logo-1536x864.png'
                  ))
