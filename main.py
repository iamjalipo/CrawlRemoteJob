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
    url = "https://justremote.co/remote-jobs"
    page_source = get_page_source(url)
    
    soup = BeautifulSoup(page_source, "html.parser")
    job_cards = soup.find_all('div', class_='new-job-item__JobItemWrapper-sc-1qa4r36-0 hxecsD')
    jobs = []

    today = datetime.today().date() 
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)


    for job in job_cards[6:]:
        posted_time = job.find('div', class_='dmIPAp')
        if posted_time:
            time_text = posted_time.text.strip()

            try:
                job_date = datetime.strptime(time_text, "%d %b").date()


                if job_date:
                    job_title = job.find('h3', class_='iNuReR').text.strip()
                    job_link = job.find('a')['href'] 
                    job_info = extract_job_details(f"https://justremote.co/{job_link}" , job_title)
                    
                    if job_info:
                        jobs.append(job_info)
                        print(f"Added job posted on {time_text}")
                    else:
                        print(f"Was not global")

                elif job_date <= two_days_ago:
                    print(f"Encountered a job posted on {time_text} (2 days ago), stopping the loop.")
                    break
            except ValueError:
                print(f"Error parsing date: {time_text}")
        
        time.sleep(1)
    
    return jobs

def extract_job_details(link , job_title):
    
    job_html = get_page_source(link)
    job_soup = BeautifulSoup(job_html, 'html.parser')

    try:
        job_type = job_soup.find('div', class_='kDMjDa').find_next('span').text.strip()
    except:
        job_type = "globally!"

    if job_type == "globally!":
        title = job_title
        company = job_soup.find('a', class_= 'jynOlu').text.strip() 
        temp = job_soup.find('div', class_='kDMjDa').text.strip() 
        workplace = (job_soup.find('div', class_='dqMVd').find_all('div'))[1].text.strip()
        applylink = job_soup.find('div', class_='hdHXKa').find_next('a')['href']
        job_dict = {
            "Title": title, #Senior QA Engineer
            "Company": company, #Super Dispatch
            "Temp": temp, #permanent
            "Type": job_type, #globally!
            "Workplace": workplace, #Fully Remote
            "Applylink" : applylink, #root_link
            "Link": link #crawl-page-link
        }
        print("*&********************************" , job_dict)
        return  job_dict
    else:
        pass

if __name__ == "__main__":
    jobs = parse_job_listings()
    if jobs:
        for job in jobs:
            print(job)
