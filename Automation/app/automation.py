# import dependencies
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, InvalidSessionIdException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import tabula, urllib3, socket, os, requests, time, random, re, logging

def create_logging():
    
    """
    Create a log file
    ---------------------------
    This function is used to create
    and configure the logging for the
    log file that stores the log messages.
    """
    
    # set logging configuration
    logging.basicConfig(filename="log_file.log", filemode='a', format='%(message)s', level=logging.INFO)
    return logging

def init_selenium():
    
    """
    Open up Chromedriver 
    -----------------------
    This method is used to initialize selenium
    chromedriver with custom configurations
    in order to crawl and scrape from the
    webpages.

    """

    # Set chromedriver configurations
    options = Options()

    # User agents for web scraping
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    
    # List of options for chromedriver
    lambda_options = [
        '--autoplay-policy=user-gesture-required',
        '--disable-background-networking',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-breakpad',
        '--disable-client-side-phishing-detection',
        '--disable-component-update',
        '--disable-default-apps',
        '--disable-dev-shm-usage',
        '--disable-domain-reliability',
        '--disable-extensions',
        '--disable-features=AudioServiceOutOfProcess',
        '--disable-hang-monitor',
        '--disable-ipc-flooding-protection',
        '--disable-notifications',
        '--disable-offer-store-unmasked-wallet-cards',
        '--disable-popup-blocking',
        '--disable-print-preview',
        '--disable-prompt-on-repost',
        '--disable-renderer-backgrounding',
        '--disable-setuid-sandbox',
        '--disable-speech-api',
        '--disable-sync',
        '--disk-cache-size=33554432',
        '--hide-scrollbars',
        '--ignore-gpu-blacklist',
        '--ignore-certificate-errors',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-default-browser-check',
        '--no-first-run',
        '--no-pings',
        '--no-sandbox',
        '--no-zygote',
        '--password-store=basic',
        '--use-gl=swiftshader',
        '--use-mock-keychain',
        '--single-process',
        'start-maximized',
        f'user-agent={user_agent}',
        '--ignore-certificate-errors',
        '--ignore-ssl-errors',
        '--disable-infobars',
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--no-sandbox']

    # restrict pdf files from automatic download
    prefs = {"download_restrictions": 3, }

    # Add all options from the list to the browser
    for argument in lambda_options:
        options.add_argument(argument)

    # Add experimental options
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", prefs)

    # Global browser to use throughout the script
    global browser
    browser = webdriver.Chrome(options=options)

    # Set page load timeput of 1 minute
    browser.set_page_load_timeout(60)


def google_search(user_input : str):
    
    """
    Perform Google Search
    ------------------------
    This method takes a user input
    and performs search on Google, 
    stores links from search results.

    Parameters
    ----------
    user_input : str
        It is the input provided by
        the user to search for.
    """
    
    # list declared to store all search result links
    all_links = []
    
    try:
        
        # Redirect to Google search URL
        browser.get('https://www.google.com/')
        
    except (TimeoutException, WebDriverException, NoSuchElementException, InvalidSessionIdException, TimeoutError, StaleElementReferenceException, ElementClickInterceptedException, requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError, socket.gaierror):
        
        logger.info("Unable to open google. Kindly check internet connection.")
        return all_links
    
    logger.info("Google opened successfully")
    
    # Wait for random time interval
    time.sleep(random.randint(10, 20))
    
    # Finds for searchbar
    search = browser.find_element(By.NAME, 'q')
    
    # Wait for random time interval
    time.sleep(random.randint(5, 8))
    
    # Search string formation
    search_string = user_input
    
    # Inputs the search string
    search.send_keys(search_string)
    
    logger.info("Search string entered in Google's search text field")
    
    # Wait for random time interval
    time.sleep(random.randint(5, 8))
    
    # Presses enter button
    search.send_keys(Keys.ENTER)
    
    # Wait for random time interval
    time.sleep(random.randint(10, 20))

    logger.info("Fetching the results from Google")

    # pagination
    while True:
        
        # Looks up for search results
        results = browser.find_elements(By.CLASS_NAME, 'g')
        
        # Condition if search results are empty
        if len(results) == 0:
            logger.info("No search results found for the query.")
            break
        
        # Condition if search results are present
        else:
            
            # Extracts links and add to the list
            links = [r.find_element(By.TAG_NAME, "a").get_attribute(
                "href") for r in results]
            
            # concatenate all the links
            all_links += links
            
            # TODO: remove this break for Google's pagination
            break
        
            # lookup for the next button and click it when found
            try:
                nxt_btn = browser.find_element(By.CSS_SELECTOR,"#pnnext .NVbCr+ span")
                nxt_btn.click()
                
                # Wait for random time interval
                time.sleep(random.randint(10, 20))
                
            except:
                break
            
    return list(set(all_links))

def format_data(soup : object):
    
    """
    Clean Soup Data
    ------------------
    This method take the soup form of page source
    and cleans it by removing unwanted blank spaces
    and extra newlines.

    Parameters
    ----------
    soup : obj
        It is the HTML soup of the webpage
    """

    # Get text from soup
    soup_text = soup.get_text(separator="\n")
    
    # Remove multiple newlines
    single_line_text = str(re.sub(r'\n+', '\n', str(soup_text)))
    
    # Remove multiple spaces
    single_space_text = [str(line).rstrip().lstrip()
                         for line in single_line_text.splitlines()]
    
    # Remove empty strings from list
    updated_list = list(filter(None, single_space_text))
    
    # Cleaned text
    cleaned_text = '\n'.join(updated_list)
    
    return cleaned_text

def get_link_source(link : str):
    
    """
    Get Page Source from Link
    -----------------------------
    This method takes link as an input, browser
    redirects to that link and the page
    source is extracted for scraping.

    Parameters
    ----------
    link : str
        Search results link form Google
        to extract the text from
    """

    try:
        
        # Browser redirects to link
        browser.get(link)
        
        # Driver waits until title of page is visible
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'title')))
        
        # Fetch page source
        ans = browser.page_source
        
    # In case of error occured while loading the link
    except (TimeoutException, WebDriverException, NoSuchElementException, InvalidSessionIdException, TimeoutError, StaleElementReferenceException, ElementClickInterceptedException, requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError, socket.gaierror):
        
        logger.info(f'Timeout Occoured loading {link}')
        return None

    try:
        # Parse the page source
        soup = BeautifulSoup(ans, 'html.parser')
        
    except:
        return None
    
    # Remove all javascript and stylesheet code
    for script in soup(["script", "style"]):
        script.extract()

    # Clean the page source soup
    text = format_data(soup)
    return text
        
        
def save_pdf_get_table_data(link : str):
    
    """
    Save PDF and Extract the table
    -----------------------------
    This method takes link as an input, and
    saves the PDF corresponding to that link.
    It also extracts the table from the PDF.

    Parameters
    ----------
    link : str
        Search results link form Google
        to extract the table from and
        save it to a folder.
    """
    
    try:
        
        # open the link
        r = requests.get(link, stream=True)
        
    except (TimeoutException, WebDriverException, NoSuchElementException, InvalidSessionIdException, TimeoutError, StaleElementReferenceException, ElementClickInterceptedException, requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError, socket.gaierror):
        
        logger.info(f"Timeout occurred opening link {link}. Could not save PDF or extract tables")
        return None
    
    # create a folder to store the PDFs
    if not os.path.exists("Pdf_Files"):
        os.makedirs("Pdf_Files")
        
    # save the PDF
    with open(f'Pdf_Files/PDF_{str(time.strftime("%Y%m%d-%H%M%S"))}.pdf', 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)
            
    logger.info("PDF file saved successfully in the Pdf_Files directory")
    
    try:
        
        # detect tables
        table = tabula.read_pdf(link,pages=1)
        
        # create a dataframe
        df = table[0]
        
        return df
    
    except:
        return None
            
def main_caller(user_input : str):
    
    """
    Main calling function
    -----------------------------
    This method is the main entry point
    and it has all the automation logic
    intact.

    Parameters
    ----------
    user_input : str
        It is the user input which is
        to be searched on the Google.
    """
    
    # script logging
    global logger
    logger = create_logging()
    
    logger.info(f"Searching for --{user_input}-- in Google")
    
    # an empty dataframe
    dataframe = pd.DataFrame(list())

    # writing empty DataFrame to the new excel file
    dataframe.to_excel('output.xlsx',index= False,)
    
    # intialize Selenium
    init_selenium()
    
    # get links from Google
    links = google_search(user_input)
    
    # final output list declared
    final_result_list = []
    
    # If links are not empty
    if len(links) > 0:
        
        # Iterate over links
        for idx, link in enumerate(links):
            
            logger.info(f"Opening link {link}")
            
            try:
                
                # open the link
                r = requests.get(link)
                
            except (TimeoutException, WebDriverException, NoSuchElementException, InvalidSessionIdException, TimeoutError, StaleElementReferenceException, ElementClickInterceptedException, requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError, socket.gaierror):
                
                logger.info(f"Timeout occurred opening link {link}. Could not check the type of the link.")
                continue
            
            try:
                
                # get the headers from the link
                content_type = r.headers.get('content-type')
                
                
            except:
                
                logger.info("Could not get the content-type of the link")
                quit()
                
            # check if the link is a pdf
            if 'application/pdf' in content_type:
                
                # save pdf file and extract tables from the PDF
                table_df = save_pdf_get_table_data(link)
                
                # If table is found
                if table_df is not None:
                    
                    # store result
                    final_result_list.append((link, f"Refer to sheet {idx+1} for table data"))
                    
                    # write result to excel file
                    with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a') as writer:  
                        table_df.to_excel(writer, sheet_name=f'{idx+1}',index= False,)
                        
                # if no table is found
                else:
                    final_result_list.append((link, "No Table data found/Unable to get table data"))
                    
            # if the link is a webpage
            else:
                
                # get the text from the link
                page_text = get_link_source(link)
                
                # if page text is extracted
                if page_text is not None:
                    
                    # store result
                    final_result_list.append((link, page_text))
                    
                # if page text is not extracted
                else:
                    
                    # store result
                    final_result_list.append((link, "Unable to get text from link"))
                
        # create a dataframe
        links_df = pd.DataFrame(final_result_list, columns =["links", "Web link text"])

        # store results to excel file
        with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a') as writer:  
            links_df.to_excel(writer, sheet_name= 'Results', index= False,)
    
    # if links are empty
    else:
        logger.info("No search results found for the query.")
        
    logger.info("--------- PROCESS FINISHED ---------")

if __name__ == '__main__':
    pass
    # user_input = str(input("Enter your search query: "))
    # main_caller(user_input)
        
    