import pytest

from web_crawler.validators.duplicate_validators import DuplicateURLValidator, DuplicatePageValidator, \
    DuplicateURLQueuedValidator


@pytest.fixture
def mock_datastore(mocker):
    return mocker.patch("web_crawler.validators.duplicate_validators.DataStore")


class TestDuplicateURLValidator:

    def test_dup_url_validator_new_url(self, mock_datastore):
        mock_url = "http://test.com"
        mock_datastore.is_url_seen.side_effect = lambda url: False if url == mock_url else True

        validator = DuplicateURLValidator(mock_datastore)

        assert validator.validate(mock_url)
        assert validator.validate("http://a.com") is False

    def test_dup_url_validator_seen_url(self, mock_datastore):
        mock_url = "http://test.com"
        mock_datastore.is_url_seen.side_effect = lambda url: True if url == mock_url else False

        validator = DuplicateURLValidator(mock_datastore)

        assert validator.validate(mock_url) is False


class TestDuplicateURLQueuedValidator:

    def test_dup_queued_url_validator_new_url(self, mock_datastore):
        mock_url = "http://test.com"
        mock_datastore.is_url_queued.side_effect = lambda url: False if url == mock_url else True

        validator = DuplicateURLQueuedValidator(mock_datastore)

        assert validator.validate(mock_url)
        assert validator.validate("http://a.com") is False

    def test_dup_url_validator_seen_url(self, mock_datastore):
        mock_url = "http://test.com"
        mock_datastore.is_url_queued.side_effect = lambda url: True if url == mock_url else False

        validator = DuplicateURLQueuedValidator(mock_datastore)

        assert validator.validate(mock_url) is False


class TestDuplicatePageFilter:

    def test_dup_page_validator_new_url(self, mock_datastore):
        mock_page_hash = "abcd123"
        mock_datastore.is_page_seen.side_effect = lambda url: False if url == mock_page_hash else True

        validator = DuplicatePageValidator(mock_datastore)

        assert validator.validate(mock_page_hash)
        assert validator.validate("123") is False

    def test_dup_page_validator_seen_url(self, mock_datastore):
        mock_page_hash = "abcd123"
        mock_datastore.is_page_seen.side_effect = lambda url: True if url == mock_page_hash else False

        validator = DuplicatePageValidator(mock_datastore)

        assert validator.validate(mock_page_hash) is False
