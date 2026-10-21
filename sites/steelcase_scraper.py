#
# Company - > Steelcase
# Link -> https://careers.smartrecruiters.com/SteelcaseInc
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county

# Steelcase este in tranzitie de platforma: joburile EMEA (Romania/Cluj) se
# publică pe SmartRecruiters, iar restul pe careers.steelcase.com
SMARTRECRUITERS_API = 'https://api.smartrecruiters.com/v1/companies/SteelcaseInc/postings'
SMARTRECRUITERS_JOB_URL = 'https://jobs.smartrecruiters.com/SteelcaseInc/'
OLD_SITE_SEARCH_URL = 'https://careers.steelcase.com/external/SearchJobs/?3_142_3=38706&folderOffset='
PAGE_SIZE = 100


def get_soup(url: str):

    res = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def get_nr_jobs():

    soup_iter = get_soup(url=OLD_SITE_SEARCH_URL + '0')
    pagination = soup_iter.find('span', class_='pagination__legend')
    if not pagination:
        return 0
    nr_jobs = int(pagination.text.split()[0])
    return nr_jobs


def get_job_types(url):

    job_type = 'on-site'

    try:
        soup = get_soup(url=url)
        text_info = soup.find('div', class_='section__content section__content--hr-top').text
    except Exception:
        return job_type

    if 'hybrid' in text_info:
        job_type = 'hybrid'
    elif 'remote' in text_info:
        job_type = 'remote'

    return job_type


def get_posting_details(posting_id):

    res = requests.get(f'{SMARTRECRUITERS_API}/{posting_id}', headers=DEFAULT_HEADERS)

    if res.status_code != 200:
        return {}

    return res.json()


def get_posting_text(details):

    sections = (details.get('jobAd') or {}).get('sections') or {}
    texts = []

    for section in sections.values():
        if isinstance(section, dict):
            texts.append(section.get('text') or '')

    return ' '.join(texts).lower()


def get_smartrecruiters_postings():
    """
    Joburile publicate in Romania pe platforma SmartRecruiters.
    """

    postings = []
    offset = 0

    while True:
        res = requests.get(SMARTRECRUITERS_API,
                           params={'country': 'ro', 'limit': PAGE_SIZE, 'offset': offset},
                           headers=DEFAULT_HEADERS)

        if res.status_code != 200:
            break

        content = res.json().get('content', [])

        if not content:
            break

        for posting in content:
            location = posting.get('location', {})

            if (location.get('country') or '').lower() != 'ro':
                continue

            postings.append(posting)

        offset += PAGE_SIZE

        if len(content) < PAGE_SIZE:
            break

    return postings


def get_smartrecruiters_job_type(location, details):

    job_type = 'on-site'

    if location.get('hybrid'):
        job_type = 'hybrid'
    elif location.get('remote'):
        job_type = 'remote'
    else:
        text_info = get_posting_text(details)

        if 'hybrid' in text_info:
            job_type = 'hybrid'
        elif 'remote' in text_info:
            job_type = 'remote'

    return job_type


def get_smartrecruiters_jobs():

    list_jobs = []

    for posting in get_smartrecruiters_postings():
        posting_id = posting.get('id')
        location = posting.get('location', {})
        details = get_posting_details(posting_id)
        link = details.get('postingUrl') or f'{SMARTRECRUITERS_JOB_URL}{posting_id}'
        city = (location.get('city') or '').strip()

        list_jobs.append({
            "job_title": posting.get('name', ''),
            "job_link": link,
            "company": "Steelcase",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": get_smartrecruiters_job_type(location, details)
        })

    return list_jobs


def get_old_site_jobs():

    list_jobs = []

    for page in range(0, get_nr_jobs(), 5):

        soup_jobs = get_soup(url=OLD_SITE_SEARCH_URL + str(page))
        jobs = soup_jobs.find_all('div', class_='list__item__text')

        for job in jobs:
            title = job.find('a').text
            link = job.find('a')['href']
            city = job.find('div', class_='list__item__text__subtitle').text.split('City:')[-1].split('.')[0].strip()

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Steelcase",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": get_job_types(link)
            })

    return list_jobs


def get_jobs():
    list_jobs = []
    seen_jobs = set()

    for job in get_smartrecruiters_jobs() + get_old_site_jobs():
        job_id = (job["job_title"].strip().lower(), job["city"].strip().lower())

        if job_id in seen_jobs:
            continue

        seen_jobs.add(job_id)
        list_jobs.append(job)

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Steelcase'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Steelcase',
                  'https://dumy1g3ng547g.cloudfront.net/content/themes/steelcase/img/logo.svg'
                  ))
