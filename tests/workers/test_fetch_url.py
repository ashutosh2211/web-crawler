import pytest

from web_crawler.fields import URLData
from web_crawler.workers.fetcher import URLFetcher


class TestURLFetchWorker:

    @pytest.fixture
    def mock_validator_generator(self, mocker):
        def _make_fixture():
            return mocker.patch("web_crawler.workers.fetcher.Validator")

        return _make_fixture()

    @pytest.fixture
    def mock_http_config(self, mocker):
        return mocker.patch("web_crawler.workers.fetcher.Config")

    @pytest.fixture
    def mock_datastore(self, mocker):
        return mocker.patch("web_crawler.workers.fetcher.DataStore")

    @pytest.fixture
    def mock_url_fetcher(self, mocker, mock_datastore, mock_http_config, mock_validator_generator):
        mock_datastore = mocker.patch("web_crawler.workers.fetcher.DataStore")
        duplicate_url_validator = mock_validator_generator()
        domain_validator = mock_validator_generator()

        return URLFetcher(
            duplicate_url_validator,
            domain_validator,
            mock_datastore,
            mock_http_config
        )

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, content, status_code, headers):
                self.content = content
                self.status_code = status_code
                self.headers = headers

            def content(self):
                return self.content

        headers = {"Content-Type": "text/html"}
        if args[1] == 'https://test.com':
            content = bytes('<p><a href="/html/tut/links.html">Basic Link</a></p>', "utf-8")
            return MockResponse(content, 200, headers)
        elif args[1] == 'https://test.com/path/1':
            content = bytes('<body>Test</body>', "utf-8")
            return MockResponse(content, 200, headers)
        else:
            return MockResponse(None, 404, headers)

    def test_execute_empty_data(self, mock_url_fetcher):
        mock_url_fetcher._data_store.get_next_url_to_fetch.return_value = None
        res = mock_url_fetcher.fetch_urls()

        assert res is None

    def test_execute_duplicate_urls(self, mock_url_fetcher):
        mock_url_data = URLData("https://test.com", bytes("<body>Test</body>", 'utf-8'))
        mock_url_fetcher._data_store.get_next_url_to_fetch.return_value = mock_url_data

        mock_url_fetcher._dup_url_validator.validate.return_value = False

        res = mock_url_fetcher.fetch_urls()

        assert res is None
        mock_url_fetcher._data_store.decrement_rem_task_count.assert_called_with()

    def test_execute_non_allowed_domain_urls(self, mock_url_fetcher):
        mock_url_data = URLData("https://test.com", bytes("<body>Test</body>", 'utf-8'))
        mock_url_fetcher._data_store.get_next_url_to_fetch.return_value = mock_url_data

        mock_url_fetcher._domain_validator.validate.return_value = False

        res = mock_url_fetcher.fetch_urls()

        assert res is None
        mock_url_fetcher._data_store.decrement_rem_task_count.assert_called_with()

    def test_execute_allowed_urls(self, mocker, mock_url_fetcher):
        mock_url_data = URLData("https://test.com", bytes("<body>Test</body>", 'utf-8'))
        mock_url_fetcher._data_store.get_next_url_to_fetch.return_value = mock_url_data

        # mock_url_fetcher.url_request.side_effect = self.mocked_requests_get
        mocker.patch.object(mock_url_fetcher, "url_request", side_effect=self.mocked_requests_get)

        mock_url_fetcher.fetch_urls()

        mock_url_fetcher._data_store.set_url_seen.assert_called_once()
        mock_url_fetcher._data_store.add_page_to_parse.assert_called_once()
        mock_url_fetcher._data_store.set_page_seen.assert_called_once()
        mock_url_fetcher._data_store.mark_url_fetch_complete.assert_called_once()

    def test_execute_allowed_urls_with_invalid_resp(self, mocker, mock_url_fetcher):
        mock_url_data = URLData("https://a.com/path/1", bytes("<body>Test</body>", 'utf-8'))
        mock_url_fetcher._data_store.get_next_url_to_fetch.return_value = mock_url_data

        mocker.patch.object(mock_url_fetcher, "url_request", side_effect=self.mocked_requests_get)
        mock_url_fetcher.fetch_urls()

        mock_url_fetcher._data_store.decrement_rem_task_count.assert_called_once()
        mock_url_fetcher._data_store.mark_url_fetch_complete.assert_called_once()
