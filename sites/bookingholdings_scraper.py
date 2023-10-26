#
#  Company - > bookingholdings
# Link -> https://jobs.bookingholdings-coe.com/careers?query=%2A&location=Bucharest%2C%20Romania&pid=562949957629221&domain=booking.com&sort_by=relevance&microsite=microsite_1
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import uuid
import requests


def get_jobs():

    list_jobs = []
    page = 0
    flag = True

    while flag:

        url = "https://jobs.bookingholdings-coe.com/api/apply/v2/jobs"
        querystring = {"domain": ["booking.com", "booking.com"],
                       "microsite": ["microsite_1", "microsite_1"],
                       "start": f"{page}",
                       "num": "10",
                       "query": "*",
                       "location": "Bucharest, Romania",
                       "pid": "562949957640563",
                       "sort_by": "relevance",
                       "triggerGoButton": "false"}
        payload = ""
        headers = DEFAULT_HEADERS

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring).json()['positions']

        if len(response) > 0:
            for job in response:
                title = job['name']
                city = job['location'].split(',')[0]
                link = f"https://jobs.bookingholdings-coe.com/careers?query=%2A&location=Bucharest%2C%20Romania&pid={job['id']}&domain=booking.com&sort_by=relevance&microsite=microsite_1"
                list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "BookingHoldings",
                    "country": "Romania",
                    "city": city,
                })
        else:
            flag = False
        page += 10

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'BookingHoldings'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('BookingHoldings',
                  'https://logowik.com/content/uploads/images/booking-holdings-inc7863.logowik.com.webp'
                  ))



