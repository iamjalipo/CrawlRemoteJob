from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)  
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break 
        last_height = new_height

def get_page_source(url):
    driver = webdriver.Chrome()
    driver.get(url)

    scroll_page(driver)
    
    page_source = driver.page_source
    driver.quit()  

    return page_source

def parse_job_listings():
    url = "https://remote.com/jobs/all?country=anywhere"
    page_source = get_page_source(url)
    
    soup = BeautifulSoup(page_source, "html.parser")
    job_cards = soup.find_all('article', class_='hoCDhn')
    jobs = []


    for job in job_cards:
        posted_time = job.find('span', class_='eNLYaf')
        if posted_time:
            time_text = posted_time.text.strip()

            if time_text == "1 day ago":
                
                job_title = job.find('span', class_='fsvfbz').text.strip()
                print("*******job_title*********" ,job_title )
                job_link = job.find('a')['href']
                print("*******job_link*********" ,job_link ) 
                try:
                    price = job.find('span', class_='iviamx').text.strip()
                except:
                    price = "Negotiable"
                job_info = extract_job_details(f"https://remote.com/{job_link}" , job_title , price)

                
                if job_info:
                    jobs.append(job_info)
                    print(f"Added job posted on {time_text}")
                else:
                    print(f"Was not global")
            elif time_text == "2 days ago":
                break

        
        time.sleep(1)
    
    return jobs

def extract_job_details(link , job_title , price):
    
    job_html = get_page_source(link)
    job_soup = BeautifulSoup(job_html, 'html.parser')
    company = job_soup.find('span', class_= 'cWvlWe').text.strip() 
    Flexibility = job_soup.find('span', class_='jvFZgN').text.strip()
    applylink = job_soup.find('dl', class_='TZgiK').find_next('a')['href']
    job_dict = {
        "Title": job_title, #Senior QA Engineer
        "Company": company, #Super Dispatch
        "Price": price, #5 dollar / hour
        "Flexibility": Flexibility, #Full-time
        "Workplace": "Fully Rmeote", #Fully Remote
        "Applylink" : applylink, #root_link
        "Link": link #crawl-page-link
    }
    return  job_dict


if __name__ == "__main__":
    jobs = parse_job_listings()
    if jobs:
        for job in jobs:
            print(job)
