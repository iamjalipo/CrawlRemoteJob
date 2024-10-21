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
python3 main.py --site justremote
```

To crawl jobs from **remote.com**:

```bash
python3 main.py --site remote
```

## How to Run Code Using run.sh

If you want to run only the **justremote.com** crawler, use the following command:

```bash
./run.sh --site justremote
```

If you want to run the **remote.com** crawler, use the following command:

```bash
./run.sh --site remote
```


