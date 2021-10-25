import pandas as pd
from RPA.Browser.Selenium import Selenium
import time
import json
import csv
from config import agency_file_path, funding_file_path, pdf_download_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


browser = Selenium()


def scrape_agency_list(url):
    """
    :param:
        url: website url
    :return: list of agency as dataframe
    """

    browser.open_available_browser(url)
    dive_in = "xpath://a[contains(text(),'DIVE IN')]"
    dive_in_button = browser.find_element(dive_in)
    dive_in_button.click()
    browser.wait_until_element_is_visible("css:#agency-tiles-widget .row .col-sm-4")
    saved_list = []
    agency_tiles = browser.find_elements("css:#agency-tiles-widget .row .col-sm-4")
    print(agency_tiles)
    for tile in range(len(agency_tiles)):
        try:
            agency_name = agency_tiles[tile].find_elements_by_css_selector("#agency-tiles-widget .h4")[0].text
            agency_expense = agency_tiles[tile].find_elements_by_css_selector("#agency-tiles-widget .row .col-sm-4 .h1")[0].text
            agency_link = agency_tiles[tile].find_elements_by_css_selector("#agency-tiles-widget .row .col-sm-4 .btn")[0].get_attribute('href')
            tile_data = [agency_name, agency_expense, agency_link]
            saved_list.append(tile_data)
        except Exception as e:
            pass
    agency_list = pd.DataFrame(saved_list, columns=["agency_name","agency_expense", "agency_link"])
    agency_list.to_csv(agency_file_path)
    browser.close_all_browsers()
    return agency_list




def scrape_investment_list(url):
    """

    :param url:
    :return: DataFrame()
    """
    browser.open_available_browser(url)
    time.sleep(20)
    investment_table = browser.find_element("id:investments-table-object_wrapper")
    Select(investment_table.find_element_by_css_selector(".c-select:nth-child(1)")).select_by_value("-1")
    time.sleep(15)

    funding_list = []
    column_list = ["UII", "UII Link", "Bureau", "Investment Title", "Total Spending", "Spending Type", "CIO Rating", "No Of Projects"]
    funding_table = browser.find_element("id:investments-table-object")
    rows = funding_table.find_elements_by_tag_name("tr")
    for row in rows:
        columns = row.find_elements_by_tag_name("td")
        if len(columns) == 7:
            UII = columns[0].text
            try:
                UII_LINK = columns[0].find_elements_by_tag_name("a")[0].get_attribute('href')
            except Exception as e:
                UII_LINK = "None"
            Bureau = columns[1].text
            investmentTitle = columns[2].text
            totalSpending = columns[3].text
            spendingType = columns[4].text
            CIORating = columns[5].text
            NoOfProjects = columns[5].text
            funding_data = [UII, UII_LINK, Bureau, investmentTitle, totalSpending, spendingType, CIORating, NoOfProjects]
            funding_list.append(funding_data)



    # browser.execute_javascript(funding_scraper)
    # data = browser.find_element('funding_data')
    # data = json.loads(data.text)

    funding_dataframe = pd.DataFrame(funding_list, columns=column_list)
    print(funding_dataframe)
    funding_dataframe.to_csv(funding_file_path)
    browser.close_browser()
    return funding_dataframe


def download_all_business_case(funding_file_path):
    """
    :param funding_file_path:
    :return: None
    """
    data = pd.read_csv(funding_file_path)
    # print(data["UII_LINK"])
    for link in data["UII Link"].items():
        if str(link[1]) != "None":
            download_business_case(link[1])

def download_business_case(funding_url):
    """
    :param funding_url:
    :return: True
    """
    funding_url = funding_url
    download_browser = Selenium()
    download_browser.set_download_directory(directory=pdf_download_path, download_pdf=True)
    download_browser.open_available_browser(funding_url)
    time.sleep(5)
    business_case_download_link = download_browser.find_element('business-case-pdf')
    business_case_download_link.click()
    time.sleep(10)
    download_browser.close_browser()
    return True


