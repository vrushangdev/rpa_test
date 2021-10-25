import pandas as pd
from RPA.Browser.Selenium import Selenium
from utils import scrape_agency_list, scrape_investment_list, download_business_case, \
     download_all_business_case
from config import challenge_website_url, funding_file_path, agency_file_path

# Preparing Assets & Required Resources
challenge_website_url = challenge_website_url
agency_website_url = ""
browser_lib = Selenium()



# Task 1 - Download List Of Agency
def download_agency_list(challenge_website_url):
    # Downloads List Of Agency
    """
    :parameter Url of Challenge Website
    :returns DataFrame Object Of Downloaded Agency List
    """
    agency_list = scrape_agency_list(url=challenge_website_url)
    return agency_list


#  Task 2 - Download Individual Investments & Business Cases
def download_individual_investments(agency_website_url):
    """
    :param agency_website_url:
    :return:
    """
    investment_list = scrape_investment_list(agency_website_url)
    download_all_business_case(funding_file_path)
    return True


# Define a main() function that calls the other functions in order:
def main():
    try:
        agency_list = download_agency_list(challenge_website_url)
        for agency in range(len(agency_list)):
            print(agency_list['agency_link'][agency])
            agency_website_url = agency_list['agency_link'][agency]
            download_individual_investments(agency_website_url)

    finally:
        browser_lib.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
