import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

def get_page(url):
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)
    return response

def parse_job_listings():
    url = "https://justremote.co/remote-jobs"
    response = get_page(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        job_cards = soup.find_all('div', class_='hxecsD')
        jobs = []

        today = datetime.today().date() 
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        print(f"**************today**************** {today}")
        print(f"**************yesterday**************** {yesterday}")
        print(f"**************two_days_ago**************** {two_days_ago}")
        
        for job in job_cards:

            parent_div = job.find_parent('div', class_='kGHzdd')
            print("*******************" , parent_div)
            if parent_div:
                print("Job found inside div with class 'kGHzdd', skipping this job.")
                continue  
            else:
                print(f"**************hiiiiiiii**************** ")
                posted_time = job.find('div', class_='dmIPAp')
                if posted_time:
                    time_text = posted_time.text.strip()

                    # Parse the date string (assuming the format is like "24 Sep")
                    job_date = datetime.strptime(time_text, "%d %b").date() 
                    print(f"**************job_date**************** {job_date}")

                    if job_date == yesterday:
                        job_title = job.find('span', class_='font-weight-bold larger').text.strip()
                        job_link = job.find('a')['href'] 

                        job_info = extract_job_details(job_link)
                        jobs.append(job_info)
                        print(f"Added job posted on {time_text}")

                    elif job_date <= two_days_ago:
                        print(f"Encountered a job posted on {time_text} (2 days ago), stopping the loop.")
                        break

                    time.sleep(1)
        
        return jobs
    
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

def extract_job_details(link):
    job_html = get_page(link)
    job_soup = BeautifulSoup(job_html.content, 'html.parser')

    title = job_soup.find('h1').text.strip() 
    location = job_soup.find('span', text='Location:').find_next('span').text.strip() 
    benefits = job_soup.find('span', text='Benefits:').find_next('span').text.strip() 
    job_type = job_soup.find('span', text='Type:').find_next('span').text.strip()
    workplace = job_soup.find('span', text='Workplace:').find_next('span').text.strip() 
    category = job_soup.find('span', text='Category:').find_next('span').text.strip() 
    description = job_soup.find('div', class_='job-description').text.strip()  

    return {
        "Title": title,
        "Location": location,
        "Benefits": benefits,
        "Type": job_type,
        "Workplace": workplace,
        "Category": category,
        "Description": description,
        "Link": link
    }

if __name__ == "__main__":
    jobs = parse_job_listings()
    if jobs:
        for job in jobs:
            print(job)
