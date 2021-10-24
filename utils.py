import pandas as pd
from RPA.Browser.Selenium import Selenium
import  time
import json
import csv
from config import agency_file_path, funding_file_path, pdf_download_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By

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


    # Sample Javascript Code.
    scrape_agency_list = """
    let saved_list = {};
    function scrape_agency_list(){
    agency_list = document.querySelectorAll("div.col-sm-4.text-center.noUnderline");
    final_list ={};
    for(var i=0;i<agency_list.length; i++ ){

      agency_name = document.querySelectorAll("div.col-sm-4.text-center.noUnderline")[i].querySelector('span.h4').innerText;
      agency_expense = document.querySelectorAll("div.col-sm-4.text-center.noUnderline")[i].querySelector('span.h1').innerText;
      agency_link = document.querySelectorAll('a.btn.btn-default.btn-sm')[0].href;
      final_list[i] = {agency_name: agency_name, agency_expense: agency_expense, agency_link: agency_link };

    }
      return final_list;
    }
    saved_list = scrape_agency_list();
    data = "<div id='agency_data'>" + JSON.stringify(saved_list) + "</div>";
    console.log(data);
    document.write(data);
    """
    # Replaced time.sleep with wait for element to load
    wait = WebDriverWait(browser, 10)
    waiting = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div.col-sm-4.text-center.noUnderline")))
    browser.execute_javascript(scrape_agency_list)
    wait.until(presence_of_element_located(By.CSS_SELECTOR, "#agency_data"))
    data = browser.find_element('agency_data')
    data = json.loads(data.text)
    print(data)
    browser.close_all_browsers()
    agency_list = data
    return agency_list


def save_agency_list(agency_list):
    """

    :param agency_list:
    :return: Dataframe of Agency List
    """
    with open(agency_file_path, 'w') as csv_data:
        column_names = ["Agency Name", "Agency Expense", "Agency Link"]
        csv_writer = csv.writer(csv_data, delimiter=',')
        csv_writer.writerow(column_names)
        for k, v in agency_list.items():
            data_row = dict(v)
            print([v['agency_name'], v['agency_expense'], v['agency_link']])
            data_row = [v['agency_name'], v['agency_expense'], v['agency_link']]
            csv_writer.writerow(data_row)
    agency_list_df = pd.read_csv(agency_file_path)
    return agency_list_df


def scrape_investment_list(url):
    """

    :param url:
    :return: DataFrame()
    """
    browser.open_available_browser(url)
    time.sleep(10)
    browser.select_from_list_by_value('investments-table-object_length', str(-1))
    time.sleep(10)

    #Execute Scraper
    funding_scraper = """
    table = document.querySelector('#investments-table-object');
    table_rows = table.tBodies[0].children[0];
    total_rows = table.tBodies[0].children.length;    
    funding_list = {};
    
    for(let i=0;i< total_rows;i++){
    
    UII = table.tBodies[0].children[i].children[0].textContent;
    try{
    UII_LINK = table.tBodies[0].children[i].children[0].children[0].href;
    }catch(err){
    UII_LINK = "None";
    }
    Bureau = table.tBodies[0].children[i].children[1].textContent;
    investment_title = table.tBodies[0].children[0].children[2].textContent;
    total_spending = table.tBodies[0].children[0].children[3].textContent;
    spending_type = table.tBodies[0].children[0].children[4].textContent;
    cio_rating = table.tBodies[0].children[0].children[5].textContent;
    no_of_projects = table.tBodies[0].children[0].children[6].textContent;
    
    funding_list[i] = {"UII": UII, "UII_LINK": UII_LINK, "Bureau": Bureau, "investment_title":investment_title, "total_spending":total_spending,"spending_type":spending_type,"cio_rating":cio_rating,"no_of_projects":no_of_projects ,};
    }
    data = "<div id='funding_data'>" + JSON.stringify(funding_list) + "</div>";
    console.log(data);
    document.write(data);    
                      """
    browser.execute_javascript(funding_scraper)
    time.sleep(10)
    data = browser.find_element('funding_data')
    data = json.loads(data.text)
    funding_dataframe = pd.DataFrame(data)
    return funding_dataframe


def download_all_business_case(funding_file_path):
    """
    :param funding_file_path:
    :return: None
    """
    data = pd.read_csv(funding_file_path)
    # print(data["UII_LINK"])
    for link in data["UII_LINK"].items():
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

def save_investment_list(funding_dataframe):
    """
    Save Funding Dataframe to CSV File in Output/Funding.csv

    :param funding_dataframe:
    :return: True
    """
    data = pd.DataFrame()
    data = funding_dataframe.transpose()
    print(data.transpose().head())
    data.to_csv(funding_file_path)
    return True