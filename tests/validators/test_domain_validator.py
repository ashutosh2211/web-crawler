import pytest

from web_crawler.validators.domain_validator import DomainValidator


@pytest.fixture
def mock_datastore(mocker):
    return mocker.patch("web_crawler.validators.duplicate_validators.DataStore")


class TestDuplicatePageFilter:

    def test_domain_validator_valid_domain(self, mock_datastore):
        allowed_domain = "test.com"
        mock_url = f"https://{allowed_domain}/test"

        mock_datastore.allowed_domains.size.return_value = 1
        mock_datastore.allowed_domains.contains.return_value = True

        validator = DomainValidator(mock_datastore)

        assert validator.validate(mock_url)

    def test_dup_page_validator_invalid_domain(self, mock_datastore):
        mock_url = "https://diff.com/test"

        mock_datastore.allowed_domains.size.return_value = 1
        mock_datastore.allowed_domains.contains.return_value = False

        validator = DomainValidator(mock_datastore)

        assert validator.validate(mock_url) is False
