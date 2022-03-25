import logging
from typing import List
from urllib.parse import DefragResult
from urllib.parse import urlparse, urldefrag

from bs4 import BeautifulSoup

from web_crawler.datastore import DataStore
from web_crawler.fields import URLData
from web_crawler.site_graph import SiteGraph
from web_crawler.validators.validator_interface import Validator

logger = logging.getLogger(__name__)


class URLParser:

    def __init__(self,
                 domain_validator: Validator,
                 dup_url_queued_validator: Validator,
                 data_store: DataStore,
                 site_graph: SiteGraph):

        self._domain_validator = domain_validator
        self._dup_url_queued_validator = dup_url_queued_validator
        self._data_store = data_store
        self._site_graph = site_graph

    def parse(self):
        url_data: URLData = self._data_store.get_next_page_to_parse()

        if not url_data:
            return

        response_html = url_data.content
        parsed_links = self.extract_links(response_html, url_data)

        for link in parsed_links:
            try:
                self._site_graph.add(url_data.url, link)
                if self._domain_validator.validate(link) and self._dup_url_queued_validator.validate(link):
                    self._data_store.add_url_to_fetch(URLData(link))
                    self._data_store.set_url_queued(link)
                    self._data_store.increment_rem_task_count()
            except Exception as exc:
                logger.exception(exc, link)
                self._data_store.add_unvisited_url(link)

        self._site_graph.add(url_data.url)
        self._data_store.decrement_rem_task_count()
        self._data_store.mark_page_parse_complete()

    def extract_links(self, resp_content: bytes, url_data: URLData):
        parser = 'html.parser'
        soup = BeautifulSoup(resp_content, parser, from_encoding=url_data.encoding)

        links = soup.find_all('a', href=True)
        filtered_links = URLParser.filter_links(links)

        links = [link["href"] for link in filtered_links]
        return self.parse_links(links, url_data.url)

    @staticmethod
    def strip_trailing_slash(url: str) -> str:
        return url.strip().rstrip("/")

    @staticmethod
    def filter_links(links):
        res = []
        for link in links:
            if link.get('href').find('tel:') > -1:
                continue
            elif link.get('href').find('mailto:') > -1:
                continue
            else:
                res.append(link)

        return res

    @staticmethod
    def parse_links(links, origin_url):
        res = set()
        for link in links:
            parsed_url = URLParser.parse_url(link, origin_url)
            if parsed_url:
                res.add(URLParser.strip_trailing_slash(parsed_url))

        return res

    @staticmethod
    def remove_fragment(url: str):
        url_res: DefragResult = urldefrag(url)
        return url_res.url

    @staticmethod
    def parse_url(url, origin_url):
        """
        :param url: url of the link
            E.g. https://monzo.com/product/1
            types of url:
                (1) complete urls: http(s)://monzo.com/blog
                (2) links with missing scheme: //monzo.com/blog
                (3) relative links: /blog/1 or blog or ../blog
        :param origin_url: url of the page from which link is parsed
        :return: parsed url complete with scheme and domain
        """
        url = URLParser.remove_fragment(url)
        url_parsed_obj = urlparse(url)
        origin_url_parsed_obj = urlparse(origin_url)

        if url_parsed_obj.scheme != "":
            # Complete url, do nothing
            return url

        elif url_parsed_obj.netloc != "":
            # missing scheme, fill with https
            parsed_obj = url_parsed_obj._replace(scheme='https')
            return parsed_obj.geturl()

        elif url_parsed_obj.path.startswith('/'):
            parsed_obj = url_parsed_obj._replace(
                scheme=origin_url_parsed_obj.scheme,
                netloc=origin_url_parsed_obj.netloc
            )
            return parsed_obj.geturl()
        else:
            path_list: List[str] = origin_url_parsed_obj.path.split('/')

            if url_parsed_obj.path.startswith('../'):
                path_list.pop()
                path_list.append(url_parsed_obj.path.lstrip('../'))
            else:
                path_list.pop()
                path_list.append(url_parsed_obj.path)

            new_path = '/'.join(path_list)
            parsed_obj = url_parsed_obj._replace(path=new_path)

            parsed_obj = parsed_obj._replace(
                scheme=origin_url_parsed_obj.scheme,
                netloc=origin_url_parsed_obj.netloc
            )
            return parsed_obj.geturl()
