#
# Company - > Edurom
# Link -> https://www.edurom.ro/it-jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county



def prepare_post():

    url = "https://www.edurom.ro/wp-admin/admin-ajax.php"

    payload = "jq=&awsm_job_spec%5Bjob-type%5D=&awsm_job_spec%5Bjob-location%5D=&awsm_job_spec%5Bjob-level%5D=&awsm_job_spec%5Bjob-status%5D=29&action=jobfilter&listings_per_page=200&shortcode_specs=job-category%3A18"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    return url, payload, headers


def get_jobs():

    list_jobs = []
    data = prepare_post()
    open_status = []
    response = requests.request("POST", data[0], data=data[1], headers=data[2])
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_='awsm-job-item')

    for job in jobs:
        title = job.find('a').text
        link = job.find('a')['href']
        list_city = job.find('div', class_='awsm-job-specification-item awsm-job-specification-job-location'
                             ).text.split()

        if len(list_city) == 1 and 'Remote' in list_city:
            city = 'Bucuresti'
            job_type = 'remote'
        elif len(list_city) == 1 and 'Hybrid' in list_city:
            job_type = 'hybrid'
            city = 'Bucuresti'
        elif len(list_city) == 1 and 'Remote' not in list_city and 'Hybrid' not in list_city:
            city = list_city
            job_type = 'on-site'

        if len(list_city) > 1 and 'Remote' in list_city:
            list_city.remove('Remote')
            city = list_city
            job_type = 'remote'
        elif len(list_city) > 1 and 'Hybrid' in list_city:
            list_city.remove('Hybrid')
            city = list_city
            job_type = 'hybrid'
        elif len(list_city) > 1 and 'Remote' not in list_city and 'Hybrid' not in list_city:
            city = list_city
            job_type = 'on-site'

        if 'from' in list_city:
            city = 'Bucuresti'
            job_type = 'remote'

        if "Cluj" in list_city:
            list_city.remove('Cluj')
            list_city.append("Cluj-Napoca")

        if "Bucharest" in list_city:
            list_city.remove('Bucharest')
            list_city.append("Bucuresti")

        list_jobs.append({
            "job_title": title,
            "job_link": link,
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


company_name = 'Edurom'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Edurom',
                  'https://images.crunchbase.com/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/v1460910381/o5sxwffz8lb8h6dpbs2b.png'
                  ))






