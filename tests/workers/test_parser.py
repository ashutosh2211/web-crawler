import pytest

from web_crawler.fields import URLData
from web_crawler.site_graph import SiteGraph
from web_crawler.workers.parser import URLParser


class TestURLParser:

    @pytest.fixture
    def mock_validator_generator(self, mocker):
        def _make_fixture():
            return mocker.patch("web_crawler.workers.parser.Validator")

        return _make_fixture()

    @pytest.fixture
    def mock_datastore(self, mocker):
        return mocker.patch("web_crawler.workers.parser.DataStore")

    @pytest.fixture
    def url_parser(self, mocker, mock_datastore, mock_validator_generator):
        mock_datastore = mocker.patch("web_crawler.workers.parser.DataStore")
        duplicate_url_queued_validator = mock_validator_generator()
        domain_validator = mock_validator_generator()
        site_graph = SiteGraph()

        return URLParser(
            domain_validator,
            duplicate_url_queued_validator,
            mock_datastore,
            site_graph
        )

    def test_execute_empty_data(self, url_parser):
        url_parser._data_store.get_next_page_to_parse.return_value = None
        res = url_parser.parse()

        assert res is None

    def test_execute_allowed_urls(self, url_parser):
        mock_url_data = URLData(
            "https://test.com",
            bytes('<p><a href="/html/tutorial/html_links">Basic Link</a></p>', "utf-8")
        )
        url_parser._data_store.get_next_page_to_parse.return_value = mock_url_data

        url_parser.parse()

        url_parser._data_store.add_url_to_fetch.assert_called_once()
        url_parser._data_store.increment_rem_task_count.assert_called_once()
        # mock_worker._data_store.set_page_seen.assert_called_once()
        # mock_worker._data_store.mark_url_fetch_complete.assert_called_once()

    def test_execute_page_resp_with_invalid_resp(self, url_parser):
        mock_url_data = URLData("https://a.com", bytes("Test</body>", 'utf-8'))
        url_parser._data_store.get_next_page_to_parse.return_value = mock_url_data

        url_parser.parse()

        assert not url_parser._data_store.add_url_to_fetch.called
        url_parser._data_store.decrement_rem_task_count.assert_called_once()
        url_parser._data_store.mark_page_parse_complete.assert_called_once()

    def test_execute_page_resp_with_no_links(self, mocker, url_parser):
        mock_url_data = URLData("https://a.com", bytes("<body>Test</body>", 'utf-8'))
        url_parser._data_store.get_next_page_to_parse.return_value = mock_url_data

        url_parser.parse()

        assert not url_parser._data_store.add_url_to_fetch.called
        url_parser._data_store.decrement_rem_task_count.assert_called_once()
        url_parser._data_store.decrement_rem_task_count.assert_called_once()
        url_parser._data_store.mark_page_parse_complete.assert_called_once()

    @pytest.mark.parametrize("url, origin_url, parsed_url",
                             [("//test.com/help", "https://test.com", "https://test.com/help"),
                              ("/help", "https://test.com", "https://test.com/help"),
                              ("https://test.com/help", "https://test.com", "https://test.com/help"),
                              ("https://test.com/help#section1", "https://test.com", "https://test.com/help"),
                              ("../help/1", "https://test.com", "https://test.com/help/1"),
                              ("help", "https://test.com", "https://test.com/help")])
    def test_parse_url(self, url, origin_url, parsed_url, url_parser):
        res = url_parser.parse_url(url, origin_url)
        assert res == parsed_url
