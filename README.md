# Cron Expression Parser

We'd like you to write a simple web crawler in a programming language you're familiar with. 
Given a starting URL, the crawler should visit each URL it finds on the same domain. It should print each URL visited, 
and a list of links found on that page. The crawler should be limited to one subdomain - so when you start with 
*https://monzo.com/*, it would crawl all pages on the monzo.com website, 
but not follow external links, for example to facebook.com or community.monzo.com.

### Usage
```shell
usage: main.py [-h] --seeds SEEDS [--allowed-domains ALLOWED_DOMAINS] [-f FORMATTER] [-o OUTPUT_FILE_NAME] 
                    [--fetch-concurrency FETCH_CONCURRENCY] [--parse-concurrency PARSE_CONCURRENCY]

A Web Crawler that starts with a set of seed url's and only follows internal links based on allowed domains

mandatory arguments:
   --seeds SEEDS
                        The initial url set from which crawling will begin. In case of multiple seed
                        urls the urls should be sparated by "|", e.g. "https://monzo.com|https://wikipedia.org"

optional arguments:
  -h, --help            show this help message and exit
                        
  --allowed-domains ALLOWED_DOMAINS
                        The set of allowed domains which would be crawled. This ignores all url's that are not in
                         the same allowed domains. In case of multiple allowed domains, they should be separated by
                         "|" e.g. "monzo.com|wikipedia.org"
                         
  -f FORMATTER
                        The output formatter (currently only yaml) which represents the structure in which 
                        the crawled and broken links are displayed.
                        
  -o OUTPUT_FILE_NAME 
                        The name of the output file where the result sets would be persisted.
                        The output directory is `outputs` within the `web-crawler` directory.
                        If argument is not given, the result set is only displayed on console.
  
  --fetch-concurrency FETCH_CONCURRENCY
                        Number of concurrent threads used for fetching url pages. 
                        Default value: 4
                        
  --parse-concurrency PARSE_CONCURRENCY
                        Number of concurrent threads used for parsing url pages.
                        Default value: 4
```
---
## How to run
The code is written for a python environment with a version of 3.7 or higher.

To install python:
```shell
➜ brew install pyenv
➜ pyenv install 3.7.0
```

To run the cli:
```
➜ cd web-crawler
➜ [web-crawler] pip install poetry==1.1.13
➜ [web-crawler] poetry install
➜ [web-crawler] poetry run python crawler.py --seeds "https://monzo.com" --allowed-domains "monzo.com" --concurrency 4
```
### Sample output
```shell
➜ [web-crawler] poetry run python main.py --seeds "https://monzo.com" --allowed-domains "monzo.com" --fetch-concurrency 4 --parse-concurrency 2 -f yaml -o output

INFO:root:Visited url count: 229
INFO:root:Visited url count: 305

https://monzo.com/usa/help:
  - https://monzo.com/blog/2021/02/22/monzo-usa-frequently-asked-questions
  - https://monzo.com/blog/monzo-us-blog
  - https://monzo.com/us
  - https://app.adjust.com/ydi27sn_9mq4ox7?engagement_type=fallback_click&fallback=https://monzo.com/download&redirect_macos=https://monzo.com/download
  - https://webviews.monzo.com/usa/terms-of-service
  - https://twitter.com/monzoUSA

unvisited_urls:
  - https://monzo.com/features
  - https://monzo.com/i
```
Unvisited URL's represent the links that were not crawled as either there was an 
error in fetching the content or the link was not an html page (e.g. an image or document).

-----
Another example
```shell
➜ [web-crawler] poetry run python main.py --seeds "https://monzo.com|https://wikipedia.org" --allowed-domains "monzo.com|wikipedia.org" --fetch-concurrency 4 --parse-concurrency 4 -f yaml -o output

INFO:root:Visited url count: 65
INFO:root:Visited url count: 105

https://monzo.com/about:
  - https://monzo.com/i/monzo-plus
  - https://monzo.com/help
  - https://monzo.com/legal/fscs-information
  - https://monzo.com/i/our-social-programme
  - https://monzo.com/about
  - https://www.youtube.com/monzobank
  - https://monzo.com/faq
  - https://app.adjust.com/ydi27sn?engagement_type=fallback_click&fallback=https%3A%2F%2Fmonzo.com%2Fdownload&redirect_macos=https%3A%2F%2Fmonzo.com%2Fdownload
  - https://www.facebook.com/monzobank
  - https://monzo.com/i/fraud
https://wikipedia.org:
  - https://lo.wikipedia.org
  - https://yi.wikipedia.org
  - https://ckb.wikipedia.org
  - https://nap.wikipedia.org
  - https://st.wikipedia.org
  - https://kg.wikipedia.org
  - https://ch.wikipedia.org
  - https://lad.wikipedia.org

unvisited_urls:
  - https://monzo.com/features
  - https://monzo.com/i
  - https://monzo.com/static/docs/modern-slavery-statement/modern-slavery-statement-2021.pdf
```

An output file is also generated with the crawled and unvisited url's in the directory `outputs` 
with the filename as provided in the `-o` option.

#### Graceful Termination
- If the process is interrupted then the crawler threads ae stopped once they have finished 
their existing tasks and the results are displayed on the console and are written
to the output file if that option was provided.
---
### Run tests
```
➜ cd web-crawler
➜ [web-crawler] poetry run pytest
```

### Run coverage
```
➜ cd web-crawler
➜ [web-crawler] poetry run coverage run -m pytest
➜ [web-crawler] poetry run coverage report
```

---
## Cases not covered
- Implementation of only scanning url's whitelisted by robots.txt has not been done.
- Politeness to reduce the number of request per domain has not been implemented.
- Add error reason for unvisited url's
