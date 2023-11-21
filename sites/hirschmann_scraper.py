#
#  Company - > hirschmann
# Link -> https://www.hirschmann-automotive.com/en/career/vacancies
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def prepare_post(offset):

    url = "https://www.hirschmann-automotive.com/en/career/vacancies"

    querystring = {"": "",
                   "tx_site_jobdetail[action]": "listApi",
                   "tx_site_jobdetail[controller]": "Job",
                   "type": "1598607815",
                   "cHash": "4ed15b391f3ac694700794122ed277ed"}

    payload = {
        "tx_site_jobdetail[__referrer][@extension]": "Site",
        "tx_site_jobdetail[__referrer][@controller]": "Job",
        "tx_site_jobdetail[__referrer][@action]": "list",
        "tx_site_jobdetail[__referrer][arguments]": "YTowOnt9282d69a51ec42845e680e4606302e3d4430e9c4b",
        "tx_site_jobdetail[__referrer][@request]": '{"@extension":"Site","@controller":"Job","@action":"list"}a041ac6c06ed0a8d742cb7d13e54c8ea259d860e',
        "tx_site_jobdetail[__trustedProperties]": '{"demand":{"jobtype":1,"location":1},"maxRecords":1,"offset":1,"detailpage":1,"cid":1}39211f8b2ce56bb127990f1f7836742847b8ee0d',
        "tx_site_jobdetail[demand][jobtype]": "",
        "tx_site_jobdetail[demand][location]": "",
        "tx_site_jobdetail[maxRecords]": 10,
        "tx_site_jobdetail[offset]": offset,
        "tx_site_jobdetail[detailpage]": 2280,
        "tx_site_jobdetail[cid]": 243
    }
    headers = {
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryOcOcokffh39CNzlZ",
    }
    return url, payload, querystring


def get_jobs():

    list_jobs = []
    offset_page = 10
    flag = True

    while flag:

        data = prepare_post(offset_page)

        response = requests.request("POST", data[0], data=data[1], params=data[2], headers=DEFAULT_HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')
        jobs = soup.find_all('li')

        if len(jobs) > 1:

            for job in jobs:
                link = 'https://www.hirschmann-automotive.com' + job.find('a')['href']
                title = job.find('h3').text
                location = job.find('a').text.split('-')[-1]
                if 'Rumänien' in location:
                    city = str(job.find('a')).split('<p>')[-1].split('-')[0].replace('Tirgu Mures', 'Târgu-Mureș'
                                                                                     ).strip()

                    list_jobs.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "hirschmann",
                        "country": "Romania",
                        "city": city,
                        "remote": 'on-site'
                    })
        else:
            flag = False
        offset_page += 10

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'hirschmann'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hirschmann',
                  'https://shop.hirschmann-automotive.com/media/image/0b/a5/6a/Automotive-Logo-quer.png'
                  ))
