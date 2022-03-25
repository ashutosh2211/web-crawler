import pytest

from web_crawler.datastore import DataStore
from web_crawler.fields import URLData


class TestDatastore:

    @pytest.fixture
    def mock_url_queue_maker(self, mocker):
        def _make_fixture():
            return mocker.patch("web_crawler.queues.queue_interfaces.QueueInterface")

        return _make_fixture()

    @pytest.fixture()
    def datastore_fixture(self, mock_url_queue_maker):
        url_fetch_queue = mock_url_queue_maker()
        content_parse_queue = mock_url_queue_maker()

        return DataStore(url_fetch_queue, content_parse_queue)

    def test_rem_task_count_increment(self, datastore_fixture):
        for i in range(5):
            datastore_fixture.increment_rem_task_count()

        assert datastore_fixture.remaining_task_count == 5

    def test_rem_task_count_increment_with_value(self, datastore_fixture):
        datastore_fixture.increment_rem_task_count(10)

        assert datastore_fixture.remaining_task_count == 10

    def test_rem_task_count_decrement(self, datastore_fixture):
        datastore_fixture.increment_rem_task_count(5)

        for _ in range(3):
            datastore_fixture.decrement_rem_task_count()

        assert datastore_fixture.remaining_task_count == 2

    def test_rem_task_count_decrement_with_value(self, datastore_fixture):
        datastore_fixture.increment_rem_task_count(15)

        for _ in range(3):
            datastore_fixture.decrement_rem_task_count(3)

        assert datastore_fixture.remaining_task_count == 6

    def test_is_url_seen_valid(self, datastore_fixture, mocker):
        seen_url = "https://test.com"

        mocker.patch.object(datastore_fixture._seen_urls, 'contains', lambda x: True)
        assert datastore_fixture.is_url_seen(seen_url)

    def test_is_url_seen_invalid(self, datastore_fixture, mocker):
        seen_url = "https://test.com"

        mocker.patch.object(datastore_fixture._seen_urls, 'contains', lambda x: False)
        assert datastore_fixture.is_url_seen(seen_url) is False

    def test_is_page_seen_valid(self, datastore_fixture, mocker):
        seen_page_hash = "abcd123"

        mocker.patch.object(datastore_fixture, "_seen_pages", {seen_page_hash})
        assert datastore_fixture.is_page_seen(seen_page_hash)

    def test_is_page_seen_invalid(self, datastore_fixture, mocker):
        seen_page_hash = "abcd123"

        mocker.patch.object(datastore_fixture, "_seen_pages", {seen_page_hash})
        assert datastore_fixture.is_page_seen("abc") is False

    def test_set_url_seen(self, datastore_fixture, mocker):
        mock_url = "https://test.com"

        datastore_fixture.set_url_seen(mock_url)

        assert mock_url in datastore_fixture.seen_urls

    def test_set_page_seen(self, datastore_fixture, mocker):
        mock_page_hash = "abcd123"

        datastore_fixture.set_page_seen(mock_page_hash)

        assert mock_page_hash in datastore_fixture.seen_pages

    def test_add_url_to_fetch(self, datastore_fixture, mocker):
        mock_data = URLData("https://test.com")

        mock_queue = mocker.patch.object(datastore_fixture._url_fetch_queue, "enqueue", mocker.MagicMock())
        datastore_fixture.add_url_to_fetch(mock_data)

        mock_queue.assert_called_with(mock_data)

    def test_add_page_to_parse(self, datastore_fixture, mocker):
        mock_data = URLData("https://test.com", bytes("<body>Test</body>", 'utf-8'))

        mock_queue = mocker.patch.object(datastore_fixture._content_parse_queue, "enqueue", mocker.MagicMock())
        datastore_fixture.add_page_to_parse(mock_data)

        mock_queue.assert_called_with(mock_data)

    def test_get_next_url_to_fetch(self, datastore_fixture, mocker):
        mock_data = URLData("https://test.com", bytes("<body>Test</body>", 'utf-8'))
        datastore_fixture._url_fetch_queue.dequeue_async.return_value = mock_data

        res = datastore_fixture.get_next_url_to_fetch()

        assert res == mock_data

    def test_get_next_page_to_parse(self, datastore_fixture, mocker):
        mock_data = URLData("https://test.com", bytes("<body>Test</body>", 'utf-8'))
        datastore_fixture._content_parse_queue.dequeue_async.return_value = mock_data

        res = datastore_fixture.get_next_page_to_parse()

        assert res == mock_data

    def test_mark_url_fetch_complete(self, datastore_fixture, mocker):
        mock_queue = mocker.patch.object(datastore_fixture._url_fetch_queue, "task_complete", mocker.MagicMock())
        datastore_fixture.mark_url_fetch_complete()

        mock_queue.assert_called_once()

    def test_mark_page_parse_complete(self, datastore_fixture, mocker):
        mock_queue = mocker.patch.object(datastore_fixture._content_parse_queue, "task_complete", mocker.MagicMock())
        datastore_fixture.mark_page_parse_complete()

        mock_queue.assert_called_once()
