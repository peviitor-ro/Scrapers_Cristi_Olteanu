#
#
#
#
#
import os
import subprocess

# exclude files
exclude = ['__init__.py',
           'A_OO_get_post_soup_update_dec.py',
           'A_OOI_main.py',
           '000_delete_api_data.py',
           'L_00_logo.py',
           'damen_scraper.py',
           'talentkompass_scraper.py',
           'ascom_scraper.py',
           'globalstep_scraper.py',
           'wyser_scraper.py',
           'visteon_scraper.py',
           'visa_scraper.py',
           'timken_scraper.py',
           'teva_scraper.py',
           'temps_scraper.py',
            'superbet_scraper.py',
            'teconnectivity_scraper.py',
           'stryker_scraper.py',
           'spearhead_scraper.py',
           'snyk_scraper.py',
            'siena_scraper.py',
            'ses_scraper.py',
            'sennder_scraper.py',
            'rws_scraper.py',
           'riverbed_scraper.py',
           'rianpartners_scraper.py',
           '_county.py',
           '_validate_city.py',
           'bayware_scraper.py'

           ]

path = os.path.dirname(os.path.abspath(__file__))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + site)
            print(errors)
        else:
            print("Success scraping " + site)
