#
# Company - > Edurom
# Link -> https://www.edurom.ro/it-jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

session = requests.Session()

def prepare_post(page: str):

    url= 'https://www.edurom.ro/wp-admin/admin-ajax.php'

    headers={
        'authority':'www.edurom.ro',
        'accept': '/',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.edurom.ro/',
        'referer': 'https://www.edurom.ro/it-jobs/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
            }

    data = {'action': 'loadmore',
            'paged': f'{page}',
            'listings_per_page': '100',
            'shortcode_specs': 'job-category%3A18'}

    return url, headers, data

def get_jobs():

    list_jobs = []

    page = 0
    flag = True

    while flag:

        data = prepare_post(str(page))
        res = requests.post(url=data[0], headers=data[1], data=data[2])
        soup = BeautifulSoup(res.text,'lxml')

        jobs = soup.find_all('div', class_='awsm-job-listing-item awsm-list-item')

        if len(jobs) > 0:


            for job in jobs:
                title = job.find('a').text
                link = job.find('a')['href']
                city = job.find('span', class_='awsm-job-specification-term').text

                try:
                    location = job.find('div',class_='awsm-job-specification-item awsm-job-specification-job-location').text
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

        else:
            flag= False
        page+=1

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






