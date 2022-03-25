import argparse
import logging

from web_crawler.config.http_config import Config
from web_crawler.crawler import WebCrawler
from web_crawler.formatter.output_factory import OutputStream
from web_crawler.validators.input_validator import SeedsAction, AllowedDomainsAction


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Domain specific Web Crawler.")
    parser.add_argument('--seeds', dest='seeds', action=SeedsAction, required=True,
                        help='''The initial URLs at which to start crawling.''')
    parser.add_argument('--allowed-domains', dest='allowed_domains', action=AllowedDomainsAction,
                        help='The list of domains that we are allowed to crawl.')
    parser.add_argument('-f', '--formatter', dest='formatter',
                        help='Print output in yaml form.')
    parser.add_argument('-o', '--output-file-name', dest='output_file_name',
                        help='''Write output to file to path `outputs/<file_name>`''')

    parser.add_argument('--fetch-concurrency', dest='fetch_concurrency', default='4',
                        help='''No. of parallel threads''')
    parser.add_argument('--parse-concurrency', dest='parse_concurrency', default='4',
                        help='''No. of parallel threads''')

    args = parser.parse_args()

    seed_urls = args.seeds
    allowed_domains = args.allowed_domains or []
    fetch_concurrency = int(args.fetch_concurrency)
    parse_concurrency = int(args.parse_concurrency)
    output_dir = "outputs"

    http_config = Config("web_crawler/config/config.yml")

    web_crawler = WebCrawler(seed_urls, fetch_concurrency, parse_concurrency, http_config,
                             allowed_domains=allowed_domains)
    site_graph, unvisited_urls = web_crawler.crawl()

    unvisited_urls_data = {"unvisited_urls": list(unvisited_urls.objs)}
    visited_urls_data = dict(site_graph.adj_list)
    combined_data = {**visited_urls_data, **unvisited_urls_data}

    if args.formatter:
        formatter = OutputStream.get_writer(args.formatter)
        formatter.write(combined_data)

    if args.output_file_name:
        writer = OutputStream.get_writer("file")
        output_filepath = f"{output_dir}/{args.output_file_name}"
        writer.write(combined_data, output_filepath)


if __name__ == "__main__":
    main()
