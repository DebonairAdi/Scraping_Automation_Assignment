# import dependencies
import re, logging, os
import pandas as pd

def create_logging():
    
    """
    Create a log file
    ---------------------------
    This function is used to create
    and configure the logging for the
    log file that stores the log messages.
    """
    
    # set logging configuration
    logging.basicConfig(filename="log_file.log", filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

    return logging

def zillow_scraper_uipath():
    
    """
    Scrape data from Zillow via UiPath
    ---------------------------
    This method is used to run the UiPath
    to scrape data from Zillow using the 
    command line interface.

    """
    
    # run the process via command line
    os.system("C:\\Users\\aditya.k\\AppData\\Local\\Programs\\UiPath\\Studio\\UiRobot.exe execute -p ZillowScraper")
    
def create_final_output_excel(results : list):
    
    """
    Generate the output excel from DF
    ---------------------------
    This method accepts a list of results
    and creates a dataframe using the results.
    Finally it generates the final output file.

    Parameters
    ----------
    results : list
        It is a list of all the results
        
    """
    
    # create a dataframe
    df = pd.DataFrame(results, columns =["Category", "House Features", "Address", "State", "Zipcode", "Price", "URL"])

    # create an excel file for the output
    df.to_excel("output.xlsx", index=False,)
    
    
if __name__ == "__main__":
    
    # script logging
    logger = create_logging()
    
    logger.info("Scraping the FOR-SALE, FOR-RENT and SOLD categories from Zillow with pagination...")
    
    # srape from zillow website
    zillow_scraper_uipath()
    
    logger.info("Records scraped successfully, creating the final output file...")

    # excel file with records scraped via UiPath
    ui_path_excel_path = "C:\\Users\\aditya.k\\.nuget\\packages\\zillowscraper\\1.0.1\\content\\Project_Notebook.xlsx"
    
    # all possible categories in Zillow/ sheet name in excel
    sheet_names_list = ["sale", "sold", "rent"]
    
    # final result list declared
    results = list()
    
    # iterate through all the excel sheets
    for sheetname in sheet_names_list:
        
        # read the excel file generated form UiPath
        df = pd.read_excel(ui_path_excel_path, sheet_name = sheetname)
        
        # iterate through all the rows in the excel file
        for idx, row in df.iterrows():
            
            # zillow categories
            category = sheetname
            
            # clean the extracted house features
            raw_features = str(row["House Features"].split("-")[0]).lstrip().rstrip()
            features = str(re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", raw_features)).replace("  ", " ")
            
            # clean the extracted address related fields
            raw_address = str(row["Address"]).split()
            address = ",".join(str(row["Address"]).split(",")[:-1])
            
            # clean the extracted zipcode and state fields
            if str(raw_address[-1]).isnumeric():
                state = str(raw_address[-2])
                zipcode = str(raw_address[-1])
            else:
                state = str(raw_address[-3])
                zipcode = " ".join(raw_address[-2:] )       
                    
            # URL of the property
            url = row["URL"]
            
            # price of the property
            price = row["Price"]
            
            # store cleaned results to the final list
            results.append((category, features, address, state, zipcode, price, url))

    # generate the final output file
    create_final_output_excel(results)
    
    logger.info("Final output generated successfully!")
    