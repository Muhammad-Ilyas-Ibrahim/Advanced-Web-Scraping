import json
import sqlite3
import os
import pyautogui
import time
import pyperclip
import random
import re

page_no = 1
page_url = None
global properties_to_scrape
properties_to_scrape = []
urls_not_scraped = []
data_path = os.path.join(os.getcwd(), 'data')
property_urls_filename = 'property_urls.txt'
property_data_filename = 'property_data.json'
agent_number_filename = 'agent_number.txt'

def create_db_if_not_exists(db_file='properties.db'):
    # Connect to SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS properties (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Page_no INTEGER,
                        URL TEXT UNIQUE,
                        Property_Name TEXT,
                        Agent_Name TEXT,
                        Agent_Contact TEXT,
                        Agent_Profile TEXT
                    )''')
     # Commit changes and close the connection
    conn.commit()
    conn.close()

def delete_urls_not_scraped():
    try:
        print("Deleting urls_not_scraped.txt file...")
        os.remove('data/urls_not_scraped.txt')
    except:
        print("urls_not_scraped.txt not found...")
        pass

def write_urls_not_scraped():
    print("Writing urls_not_scraped list to file...")
    if len(urls_not_scraped) > 0:
        with open(f'data/urls_not_scraped.txt', 'w') as file:
            for url in urls_not_scraped:
                file.write(url + '\n')
        print("URLs not scraped have been saved to urls_not_scraped.txt")  
        
def read_urls_not_scraped():
    print("Reading urls_not_scraped list from file...")
    with open(f'data/urls_not_scraped.txt', 'r') as file:
        urls = file.readlines()
        for url in urls:
            properties_to_scrape.append(url.strip())

def check_console():
    print("Verifying console status...")
    tries = 0
    while True:
        if tries == 5:
            print("Could not activate console. Exiting...")
            exit()
        # Locate the image on the screen
        active_console = None
        try:
            active_console = pyautogui.locateOnScreen('active_console.png', confidence=0.7)
            pyautogui.moveTo(active_console)
            pyautogui.click()
            print('Console is active.')
        except:
            try:
                inactive_console = pyautogui.locateOnScreen('inactive_console.png', confidence=0.7)
                pyautogui.moveTo(inactive_console)
                pyautogui.click()
                active_console = inactive_console
            except:
                print("Could not find the console. Retrying...")
                time.sleep(1)
        if active_console: 
            return active_console
        else:
            print("Console is inactive. Activating...")
            time.sleep(1)  
        tries += 1
        
def update_page_url(page_no):
    global page_url
    page_url = f'https://www.99.co/singapore/rent/condos-apartments?bathrooms=any&building_age=any&composite_floor_level=any&composite_furnishing=any&composite_views=any&diversity_friendly=false&features_and_amenities=any&has_floor_plan=false&main_category=condo&page_num={page_no}&page_size=36&path=%2Fsingapore%2Frent%2Fcondos-apartments&period_of_availability=any&property_segments=residential&rental_type=all&rooms=any&show_cluster_preview=true&show_description=true&show_internal_linking=true&show_meta_description=true&show_nearby=true&sort_field=distribution_score&sort_order=desc'
    

# Load JSON data from file
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error: {e}")
        return None

def delete_json_files():
    path = 'data/'
    try:
        # List all files in the path
        for filename in os.listdir(path):
            # Create the full path to the file
            file_path = os.path.join(path, filename)
            
            # Check if it's a JSON file
            if filename.endswith('.json'):
                # Delete the JSON file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def url_exists_in_db(url, db_file='properties.db'):
    count = 0
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM properties WHERE URL = ?", (url,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    db_file = 'real_estate_agents.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM properties WHERE URL = ?", (url,))
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0

# Write data to SQLite3 database
def write_to_db(data, page_no, db_file='properties.db'):
    print("Writing data to database...")
    # Connect to SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS properties (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Page_no INTEGER,
                        URL TEXT UNIQUE,
                        Property_Name TEXT,
                        Agent_Name TEXT,
                        Agent_Contact TEXT,
                        Agent_Profile TEXT
                    )''')

    # Insert data into table
    if data:
        for item in data:
            if all(key in item for key in ('pageURL', 'propertyName', 'agentName', 'agentContact', 'agentProfile')):
                cursor.execute('''INSERT OR IGNORE INTO properties (Page_no, URL, Property_Name, Agent_Name, Agent_Contact, Agent_Profile)
                                VALUES (?, ?, ?, ?, ?, ?)''', 
                            (page_no, item['pageURL'], item['propertyName'], item['agentName'], item['agentContact'], item['agentProfile']))
            else:
                print(f"Missing data in item: {item}")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def handle_db():
    try:
        json_file_path = os.path.join(data_path, property_data_filename)  
        print(f"Reading {property_data_filename} file...")
        data = load_json_file(json_file_path)
    except FileNotFoundError:
        print(f"{property_data_filename} not found.")
        return False
    if data is not None:
        print("Data found in JSON file...")
        print("=================================================")
        print(f"URL: {data[0]['pageURL']}")
        print(f"Property Name: {data[0]['propertyName']}")
        print(f"Agent Name: {data[0]['agentName']}")
        print(f"Agent Contact: {data[0]['agentContact']}")
        print(f"Agent Profile: {data[0]['agentProfile']}")
        print("=================================================")
        
        write_to_db(data, page_no)
        print("Data has been written to the SQLite3 database...")
        delete_json_files()
        return True
    
def find_number_in_db(agentProfile):
    # Define the databases and table name
    db_files = ["properties.db", "profiles_and_numbers.db"]
    table_name = "properties"
    
    for db_file in db_files:
        # Connect to the database
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Query to search for agentProfile in the table
            query = f"SELECT Agent_Contact FROM {table_name} WHERE Agent_Profile = ?"
            cursor.execute(query, (agentProfile,))
            
            result = cursor.fetchone()
            
            # If a match is found, return the AgentContact
            if result:
                conn.close()
                return result[0]  
            
            conn.close()
            
        except:
            pass
    
    return None

def check_agent_profile_in_db():
    with open(f'data/{property_data_filename}', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        agent_profile = item['agentProfile']
    agent_contact = find_number_in_db(agent_profile)
    if agent_contact:
        for item in data:
            item['agentContact'] = agent_contact
        print("Agent profile found in database. Merging data...")
        with open(f'data/{property_data_filename}', 'w', encoding='utf-8') as file:
            json.dump(data, file)
        return True
    return False
    
def open_url(url):
    command = f'window.location.href = "{url}";'
    pyperclip.copy(command)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'enter')    
    time.sleep(random.randint(10, 13))
    
def wait_for_urls():
    print("Waiting for urls...")
    time.sleep(2)
    n = 0
    while n < 3:
        if os.path.exists(f'data/{property_urls_filename}'):
            print("Results found")
            break
        time.sleep(2)
        n += 1
        
def wait_for_details():
    print("Waiting for details...")
    time.sleep(1)
    n = 0
    while n < 3:
        if os.path.exists(f'data/{property_data_filename}'):
            print("Results found")
            try:
                with open(f'data/{property_data_filename}', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if len(data) > 0:
                        for item in data:
                            if item['agentProfile'] is not None:                            
                                return True
                            else:
                                return 3
                    else:
                        return 404
            except:
                return False
            break
        time.sleep(2)
        n += 1
        
def wait_for_number():
    print("Waiting for number...")
    time.sleep(2)
    while True:
        if os.path.exists(f'data/{agent_number_filename}'):
            print("Results found")
            break
        time.sleep(2)
        
def prepare_urls():
    print(f"Reading {property_urls_filename} file...")
    try:
        with open(f'data/{property_urls_filename}', 'r') as file:
            urls = file.readlines()
            for url in urls:
                properties_to_scrape.append(url.strip())
    except:
        print(f"Could not read {property_urls_filename}...")
        return
            
# To keep track of the pages left to scrape, if programe crashes we can start from where we left
def rewrite_urls_file():
    try:
        print(f"Rewriting {property_urls_filename} file...")
        with open(f'data/{property_urls_filename}', 'w') as file:
            for url in properties_to_scrape:
                file.write(url + '\n')
    except:
        print(f"Could not rewrite {property_urls_filename}...")
        time.sleep(1.5)
        rewrite_urls_file()
            
def update_page_no(page_no):
    with open('data/page_no.txt', 'w') as file:
        file.write(str(page_no))
             
def wait_for_save_prompt(filename):
    print("Waiting for save prompt...")
    tries = 0
    while True:
        if tries == 5:
            print("Save prompt not found. Exiting...")
            return True
        # Locate the image on the screen
        image_location = None
        try:
            image_location = pyautogui.locateOnScreen('save.png', confidence=0.7)
        except:
            pass        
        if image_location:
            # Image found
            time.sleep(0.5)
            print("Save Button Found.")
            pyperclip.copy(os.path.join(data_path, filename))
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'enter')  
            return False 
        else:
            print("Save prompt not found. Retrying...")
            time.sleep(2)  
        tries += 1

def indicate():
    # Define the pattern using regular expressions (e.g., Page_no_<number>_urls_left_<number>.txt)
    pattern = r'^Page_\d+_urls_\d+\.txt$'

    # Get the list of files in the 'data' directory
    for file_name in os.listdir('data'):
        # Check if the file name matches the pattern
        if re.match(pattern, file_name):
            # Construct the full file path
            file_path = os.path.join('data', file_name)
            try:
                # Delete the matching file
                os.remove(file_path)
                print(f'Deleted: {file_path}')
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
    with open(f'data/Page_{page_no}_urls_{len(properties_to_scrape)}.txt', 'w') as file:
       file.write('')

def scrape_agent_number_and_merge_in_data():
    with open(f'data/{property_data_filename}', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        agent_profile = item['agentProfile']
        
    print("Opening agent profile URL... ")    
    open_url(agent_profile)
    # Click Show number button
    with open('scripts/scrape_number.js', 'r', encoding='utf-8') as file:
        scrape_number_code = file.read()
    print("Executing script to scrape agent number...")
    pyperclip.copy(scrape_number_code)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(1)
    pyautogui.write('clickshowButton();', interval=0.03)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(1)
    
    # scrape number
    pyautogui.write('scrape_and_export_number();', interval=0.03)
    pyautogui.hotkey('ctrl', 'enter')
    response = wait_for_save_prompt(agent_number_filename)
    if response:
        return True
    wait_for_number()
    
    with open(f'data/{agent_number_filename}', 'r') as file:
        agent_number = file.read()
    try:
        os.remove(f'data/{agent_number_filename}')
    except:
        pass
    if 'Oh no!' in str(agent_number):
        print("Number not found. Skiping URL...")
        print(f"Deleting {property_data_filename} file...")
        try:
            os.remove(f"data/{property_data_filename}")
        except:
            pass
        return 404
        
    if 'Show' in str(agent_number):
        print("Show button didn't work. Skiping URL...")
        return True
    
    for item in data:
        item['agentContact'] = agent_number
    with open(f'data/{property_data_filename}', 'w', encoding='utf-8') as file:
        json.dump(data, file)
    return False

def scrape_property(url):
    console_axis = check_console()
    print("Navigating to the console, please avoid moving the mouse pointer.")
    pyautogui.moveTo(console_axis)
    pyautogui.click()
    print("Deleting JSON files if exist...")
    delete_json_files()
    # print(f"Checking and Removing duplicate URLs from {property_urls_filename}...")
    # remove_duplicate_urls()
    print("Opening URL: ", url)
    open_url(url)
    indicate()
    print("Executing script to scrape property details...")
    pyperclip.copy(scrape_details_code)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(1.5)
    pyautogui.write('clickShowButton();', interval=0.03)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(3)
    pyautogui.write('extractData();', interval=0.03)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(2)
    pyautogui.write('exportData();', interval=0.03)
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(1)
    response = wait_for_save_prompt(property_data_filename)
    if response:
        print("Deleting url from properties_to_scrape list: ", url)
        properties_to_scrape.pop(0)
        return            
    response = wait_for_details()
    if response:
        pass
    else:
        print("Deleting url from properties_to_scrape list: ", url)
        properties_to_scrape.pop(0)
        return
    print("Now I will write data to database...")
    response = handle_db()
    if not response:
        print("Deleting url from properties_to_scrape list: ", url)
        properties_to_scrape.pop(0)
        return
    print("Removing URL from properties_to_scrape list...")
    properties_to_scrape.pop(0)
     
    if check_properties_list():
        return    

    
def check_properties_list():
    global properties_to_scrape
    
    print("Deleting JSON files...")
    delete_json_files()       
    if len(properties_to_scrape) == 0:
        print("All URLs have been scraped.")
        try:
            os.remove(f'data/{property_urls_filename}')
        except FileNotFoundError:
            print(f"{property_urls_filename} not found")
        return True
    else:
        print("Rewriting URLs file...")
        properties_to_scrape = list(set(properties_to_scrape))
        rewrite_urls_file()  
        print("Page no: ", page_no)
        print("Total URLs left to scrape: ", len(properties_to_scrape)) 
        return False   
             
def scrape_properties(scrape_details_code):
    console_axis = check_console()
    for url in properties_to_scrape[:]:
        if url_exists_in_db(url):
            print(f"URL already exists in database: {url}")
            print("Removing from list...")
            properties_to_scrape.pop(0)
            if check_properties_list():
                break
            else:
                continue   
            
        print("Navigating to the console, please avoid moving the mouse pointer.")
        pyautogui.moveTo(console_axis)
        pyautogui.click()
        print("Deleting JSON files if exist...")
        delete_json_files()
        # print(f"Checking and Removing duplicate URLs from {property_urls_filename}...")
        # remove_duplicate_urls()
        print("Opening URL: ", url)
        open_url(url)
        indicate()
        print("Executing script to scrape property details...")
        pyperclip.copy(scrape_details_code)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.5)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(1.5)
        pyautogui.write('extractData();', interval=0.03)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(2)
        pyautogui.write('exportData();', interval=0.03)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(1)
        response = wait_for_save_prompt(property_data_filename)
        
        if response:
            urls_not_scraped.append(url)
            print("Save prompt not found. Skiping URL..")
            print("URL: ", url)
            print("Adding URL to urls_not_scraped list...")
            print("URLs in urls_not_scraped list: ", len(urls_not_scraped))
            write_urls_not_scraped()
            print("Deleting url from properties_to_scrape list: ", url)
            properties_to_scrape.pop(0)
            if check_properties_list():
                    break
            else:
                continue   
            
        if response := wait_for_details():
            if response == 3:
                print("Agent profile not found. Skiping URL...")
                print("Deleting url from properties_to_scrape list: ", url)
                properties_to_scrape.pop(0)
                if check_properties_list():
                    break
                else:
                    continue   
            elif response == 404:
                print("Page not found Or missing Agent Data... Skiping URL...")
                print("Deleting url from properties_to_scrape list: ", url)
                properties_to_scrape.pop(0)
                if check_properties_list():
                    break
                else:
                    continue       
            else:
                print(f"{property_data_filename} found...")
                if check_agent_profile_in_db():
                    time.sleep(2)
                    handle_db()
                    print("Deleting url from properties_to_scrape list: ", url)
                    properties_to_scrape.pop(0)
                    if check_properties_list():
                        break
                    else:
                        continue   
        else:
            urls_not_scraped.append(url)
            print(f"{property_data_filename} not found. Skiping URL..")
            print("URL: ", url)
            print("Adding URL to urls_not_scraped list...")
            print("URLs in urls_not_scraped list: ", len(urls_not_scraped))
            write_urls_not_scraped()
            print("Deleting url from properties_to_scrape list: ", url)
            properties_to_scrape.pop(0)
            if check_properties_list():
                break
            else:
                continue   
     
        print("Navigating to the console, please avoid moving the mouse pointer.")
        pyautogui.moveTo(console_axis)
        pyautogui.click()
        time.sleep(1)
        
        # Scrape agent number
        print("Now I will scrape agent number...")
        response = scrape_agent_number_and_merge_in_data()
        if response:
            if response == 404:
                print("Number not found. Trying to scrape from main page...")
                try:
                    os.remove(f'data/{property_data_filename}')
                except: 
                    pass
                scrape_property(url)
                if check_properties_list():
                    break
                else:
                    continue   
            else:
                urls_not_scraped.append(url)
                print(f"{agent_number_filename} not found. Skiping URL..")
                print("URL: ", url)
                print("Adding URL to urls_not_scraped list...")
                print("URLs in urls_not_scraped list: ", len(urls_not_scraped))
                write_urls_not_scraped()
                print("Deleting url from properties_to_scrape list: ", url)
                properties_to_scrape.pop(0)
                if check_properties_list():
                    break
                else:
                    continue   
        
        print("Agent number has been scraped and merged in data...")
        print("Trying to write data to database...")
        handle_db()
        print("Removing URL from properties_to_scrape list...")
        properties_to_scrape.pop(0)
        if check_properties_list():
            break
            
# Main function
if __name__ == "__main__":
    scrape_details_code = None
    scrape_urls_code = None
    page_no = 1
    
    create_db_if_not_exists()
    
    with open('data/page_no.txt', 'r') as file:
        page_no = int(file.read().strip())
    update_page_url(page_no)
    
    with open('scripts/scrape_urls.js', 'r', encoding='utf-8') as file:
        scrape_urls_code = file.read()
        
    with open('scripts/scrape_details.js', 'r', encoding='utf-8') as file:
        scrape_details_code = file.read()
    
    print("Please go to console of browser and leave the cursor there before timer reaches to 0")
    print(f'Page no: {page_no}')
    print(f"Page URL: {page_url}")
    
    input("Press Enter to start scraping...")
    num = 5
    while num > 0:
        print("Starting in ", num, " seconds...", end='\r')
        time.sleep(1)
        num -= 1
    print("\nStarting now...")
    delete_json_files()
    
    if os.path.exists('data/urls_not_scraped.txt'):
        print("urls_not_scraped.txt file found...")
        read_urls_not_scraped()
        delete_urls_not_scraped()
        if os.path.exists(f'data/{property_urls_filename}'):
            print("Property URLs file found as well...")
            prepare_urls()
            rewrite_urls_file()
        
    if os.path.exists(f'data/{property_urls_filename}'):
        print("Property URLs file found...")
        print("Resuming from where we left...")
        prepare_urls()
        check_console()
        scrape_properties(scrape_details_code)
        tries = 0
        while len(urls_not_scraped) > 0 and tries < 3:
            if os.path.exists('data/urls_not_scraped.txt'):
                read_urls_not_scraped()
                delete_urls_not_scraped()
                urls_not_scraped.clear()
                
                scrape_properties(scrape_details_code)
                tries += 1
        page_no += 1    
        update_page_no(page_no)
    start = page_no    
    for _ in range(start, 447):
        if os.path.exists(f'data/{property_urls_filename}'):
            print("Property URLs file found...")
            print(f"Deleting {property_urls_filename} file...")
            try:
                os.remove(f'data/{property_urls_filename}')
            except:
                print("Something went wrong while deleting the file.")
                exit()
        update_page_url(page_no)
        print(f"Scraping page no {page_no} | URL: {page_url}")
        open_url(page_url)
        check_console()
        time.sleep(2)
        print("Executing script to scrape URLs...")
        pyperclip.copy(scrape_urls_code)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.5)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(1.5)
        print("Scraping URLs from main page...")
        pyautogui.write('startScraping();', interval=0.05)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'enter')
        
        response = wait_for_save_prompt(property_urls_filename)
        if response:
            print("Save prompt not found. Trying again...")
            continue
        
        wait_for_urls()
        prepare_urls()
        scrape_properties(scrape_details_code)
        os.system('ipconfig /flushdns')
        tries = 0
        while len(urls_not_scraped) > 0 and tries < 2:
            if os.path.exists('data/urls_not_scraped.txt'):
                read_urls_not_scraped()
                delete_urls_not_scraped()
                urls_not_scraped.clear()
                
                scrape_properties(scrape_details_code)
                tries += 1
            
        page_no += 1
        update_page_no(page_no)
        os.system('ipconfig /flushdns')