#
#
#
# This Decorator will avoid duplicate for me!
# Respect DRY
# This decorator have: default headers and soup and update data on peviitor.ro!
#
import requests
#
import os  # I do not have API KEY
#
import json

from A_OO_empty_jobs_repair import NO_JOBS_MARKER, maybe_repair_empty_jobs_output


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Refer': 'https://google.com',
    'DNT': '1'
}


########### UPDATE API DECORATOR ############
def update_peviitor_api(original_function):
    """
    Decorator for update data on Peviitor.ro API
    """

    def new_function(*args, **kwargs):
        company_name, data_list = args
        #
        token = get_token()
        post_header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }
        validator_endpoint = 'https://api.laurentiumarian.ro/jobs/add/'

        if not data_list:
            print(f"{company_name} (0 joburi) - nicio pozitie disponibila")
            print(f"Data for {company_name} - no jobs found.")
            # markerul se tipareste inainte de hook: repararea reusita se
            # incheie cu SystemExit(0) si ar suprima orice print de dupa el
            print(f"{NO_JOBS_MARKER} {company_name}", flush=True)
            maybe_repair_empty_jobs_output(company_name)
        else:
            res = requests.post(validator_endpoint,
                                json=data_list, headers=post_header)
            print(json.dumps(data_list, indent=4))
            if res.status_code == 200:
                print(f"Data for {company_name} updated successfully on Peviitor API!")
            else:
                print(
                    f"Failed to update data for {company_name} on Peviitor API. Status code: {res.status_code}, Response: {res.text}")

        return original_function(*args, **kwargs)

    return new_function


def get_token():
    token_endpoint = 'https://api.laurentiumarian.ro/get_token'

    token = requests.post(token_endpoint, json={
        "email": "cristiolteanu1892@gmail.com"
    }, headers = {
    "Content-Type": "application/json",
})

    return token.json()['access']
