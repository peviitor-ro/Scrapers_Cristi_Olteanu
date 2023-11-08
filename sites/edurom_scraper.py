#
# Company - > Edurom
# Link -> https://www.edurom.ro/it-jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def prepare_post():

    url = "https://www.edurom.ro/wp-admin/admin-ajax.php"

    payload = "jq=&awsm_job_spec%5Bjob-type%5D=&awsm_job_spec%5Bjob-location%5D=&awsm_job_spec%5Bjob-level%5D=&awsm_job_spec%5Bjob-status%5D=29&awsm_job_spec%5Bjob-requirements%5D=&action=jobfilter&listings_per_page=100&shortcode_specs=job-category%3A18"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    return url, payload, headers


def get_jobs():

    list_jobs = []
    data = prepare_post()

    response = requests.request("POST", data[0], data=data[1], headers=data[2])
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_='awsm-job-listing-item awsm-list-item')

    for job in jobs:
        title = job.find('a').text
        link = job.find('a')['href']
        city = job.find('span', class_='awsm-job-specification-term').text
        location = ''

        try:
            location = job.find('div', class_='awsm-job-specification-item awsm-job-specification-job-location').text
        except:
            pass

        if 'Remote' in location:
            remote = 'remote'
        elif 'Hybrid' in location:
            remote = 'hybrid'
        else:
            remote = 'on-site'

        if city == 'Hybrid':
            city = location.split()[-1]

        if city != 'Closed' and city != 'Senior':
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Edurom",
                "country": "Romania",
                "city": city,
                "remote": remote
            })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Edurom'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Edurom',
                  'https://images.crunchbase.com/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/v1460910381/o5sxwffz8lb8h6dpbs2b.png'
                  ))






