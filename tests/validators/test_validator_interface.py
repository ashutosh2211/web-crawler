import pytest

from web_crawler.validators.validator_interface import Validator


class TestValidatorInterface:

    def test_validator_interface_raises_exc_if_interface_called(self):

        with pytest.raises(NotImplementedError) as exc:
            # validator = Validator()
            Validator.validate(None, "abc")

        assert "An implementation of this class is needed" == str(exc.value)
