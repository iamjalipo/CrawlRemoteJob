import argparse
from crawlers.justremote import JustRemoteCrawler
from crawlers.remote import RemoteComCrawler

def main():
    parser = argparse.ArgumentParser(description="Crawl job listings from different websites")
    parser.add_argument('--site', choices=['justremote', 'remote'], required=True, help="The site to crawl (justremote or remote)")

    args = parser.parse_args()

    if args.site == 'justremote':
        crawler = JustRemoteCrawler()
        jobs = crawler.parse_job_listings()
    elif args.site == 'remote':
        crawler = RemoteComCrawler()
        jobs = crawler.parse_job_listings()

    print(f"Crawled {len(jobs)} jobs")

if __name__ == "__main__":
    main()
