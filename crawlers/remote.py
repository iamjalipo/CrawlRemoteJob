from selenium import webdriver
from bs4 import BeautifulSoup
import time

class RemoteComCrawler:
    def __init__(self):
        self.jobs = []

    def scroll_page(self, driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_page_source(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        self.scroll_page(driver)
        page_source = driver.page_source
        driver.quit()
        return page_source

    def extract_job_details(self, link, job_title, price):
        job_html = self.get_page_source(link)
        job_soup = BeautifulSoup(job_html, 'html.parser')
        company = job_soup.find('span', class_='cWvlWe').text.strip()
        Flexibility = job_soup.find('span', class_='jvFZgN').text.strip()
        applylink = job_soup.find('dl', class_='TZgiK').find_next('a')['href']
        job_dict = {
            "Title": job_title,
            "Company": company,
            "Price": price,
            "Flexibility": Flexibility,
            "Workplace": "Fully Remote",
            "Applylink": applylink,
            "Link": link
        }
        return job_dict

    def parse_job_listings(self):
        url = "https://remote.com/jobs/all?country=anywhere"
        page_source = self.get_page_source(url)

        soup = BeautifulSoup(page_source, "html.parser")
        job_cards = soup.find_all('article', class_='hoCDhn')

        for job in job_cards:
            posted_time = job.find('span', class_='eNLYaf')
            if posted_time:
                time_text = posted_time.text.strip()

                if time_text == "1 day ago":
                    job_title = job.find('span', class_='fsvfbz').text.strip()
                    job_link = job.find('a')['href']
                    try:
                        price = job.find('span', class_='iviamx').text.strip()
                    except:
                        price = "Negotiable"
                    job_info = self.extract_job_details(f"https://remote.com/{job_link}", job_title, price)

                    if job_info:
                        self.jobs.append(job_info)
                        print(f"Added job posted on {time_text}")
                    else:
                        print(f"Was not global")
                elif time_text == "2 days ago":
                    break
            time.sleep(1)

        return self.jobs
