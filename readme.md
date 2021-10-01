## RPA Challenge (Task Definition)


### Get List Of Agencies
#### Steps to Accomplish Task
- [x] open browser
- [x] find dive In button
- [x] click dive in
- [x] find elements
- [x] get list of agencies
- [x] get list of spent amount
- [x] save data to a spreadsheet 

#### Key Resources For This Task
- challenge_website_url : https://itdashboard.gov
- agency_file_path: output/Agencies.csv

#### Code Implementation (Big Picture)
```py
def download_agency_list():
    agency_list = scrape_agency_list(challenge_website_url)
    save_agency_list(agency_list)
```

### Get List Of Individual Investments with Business CASE PDF (If Present)
#### Steps to Accomplish Task
- [X] Select One Agency
- [X] Go to Agency Page
- [X] Find Individual Investment Table
- [X] Scrape Table and write to new excel file
- [X] If UII column contains link
- [X] open link
- [X] download pdf with "Download Business CASE PDF"
- [X] Store & download files to output folder

#### Key resources for this task
- Agency Website URL (From Agency Link Column In agency_file_path) 
- > Example Agency Link/Website: https://itdashboard.gov/drupal/summary/005
- individual_investment_file_path: output/IndividualInvestment.csv
- business_case_file_path: output/pdfs

```py
def download_individual_investments():
    investment_list = scrape_investment_list(agency_website_url)
    download_business_case(investment_list)
    save_investment_list(investment_list)
```

"# rpa_test" 
