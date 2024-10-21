# CrawlRemoteJob

This project crawls remote job postings from two websites: `justremote.co` and `remote.com`.

## Directory Structure

```
CrawlRemoteJob/
├── crawlers/
│   ├── justremote.py
│   ├── remote.py
├── main.py
├── run.sh
└── README.md
```

## Requirements

- Python 3.x
- Install the required packages using `pip`

`beautifulsoup4` `selenium`

## How to Run Code Using Python Command

Run the script manually with a site flag:

To crawl jobs from **justremote.com**:

```bash
pip install selenium beautifulsoup4
```

```bash
python main.py --site justremote
```

To crawl jobs from **remote.com**:

```bash
python main.py --site remote
```



